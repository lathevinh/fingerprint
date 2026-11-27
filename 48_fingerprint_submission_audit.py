"""Verify saved NBIS reports and bootstrap paired deltas without rerunning tests."""

import argparse
import hashlib
import io
import json
from pathlib import Path
from zipfile import ZipFile

import numpy as np
import pandas as pd


METHODS = ("native_l1", "native_triplet")
KEYS = ["pair_id", "dataset", "db", "label", "probe_identity", "gallery_identity", "probe_path", "gallery_path"]


class Report:
    def __init__(self, archive):
        self.archive = archive
        top, = [name for name in archive.namelist()
                if name.count("/") <= 1 and name.split("/")[-1] == "completion.json"]
        self.root = top.removesuffix("completion.json")
        self.marker = json.loads(archive.read(top))

    def checked(self, name, digest):
        data = self.archive.read(self.root + name)
        if hashlib.sha256(data).hexdigest() != digest:
            raise ValueError(f"Checksum mismatch: {name}")
        return data

    def summary(self, name):
        return pd.read_csv(io.BytesIO(self.checked(name, self.marker["file_sha256"][name])))

    def scores(self, method):
        return self.severe_variant(method, "scores.csv")

    def severe_variant(self, method, name):
        unit = f"dry_like_severe_{method}"
        marker = json.loads(self.checked(
            f"{unit}/completion.json", self.marker["unit_completion_sha256"][unit]))
        if marker["variant"] != unit or marker["configuration_sha256"] != self.marker["configuration_sha256"]:
            raise ValueError(f"Incorrect score provenance: {unit}")
        return pd.read_csv(io.BytesIO(self.checked(f"{unit}/{name}", marker["file_sha256"][name])))

    def decisions(self):
        config = json.loads(self.checked("configuration.json", self.marker["configuration_sha256"]))
        expected = {(r["dataset"], r["db"]): tuple(r[m] for m in METHODS) for r in config["thresholds"]}
        a, b = [self.scores(m).sort_values("pair_id").reset_index(drop=True) for m in METHODS]
        if a["pair_id"].duplicated().any() or not a[KEYS].equals(b[KEYS]):
            raise ValueError("Methods have different or duplicate pairs")
        if not a["label"].isin([0, 1]).all() or not a["label"].eq(a["probe_identity"].eq(a["gallery_identity"])).all():
            raise ValueError("Unexpected pair labels")
        result = a[KEYS].copy()
        for i, frame in enumerate((a, b)):
            threshold = [expected[(dataset, db)][i] for dataset, db in zip(frame.dataset, frame.db)]
            matchable = frame["matchable"]
            if not pd.api.types.is_bool_dtype(matchable) or frame.loc[matchable, "score"].isna().any():
                raise ValueError("Invalid matchability or missing valid NBIS score")
            result[f"score_{i}"] = frame["score"]
            result[f"threshold_{i}"] = threshold
            result[f"accept_{i}"] = matchable & frame["score"].ge(threshold)
        return result


def severe_counts(report):
    rows = report.summary("paired_attempt_changes.csv").query("condition == 'dry_like/severe'")
    metrics = report.summary("test_metrics.csv").query(
        "condition == 'dry_like/severe' and view == 'all_impressions'").set_index(["dataset", "db", "method"])
    if rows.empty or rows.duplicated(["dataset", "db"]).any() or len(metrics) != 2 * len(rows):
        raise ValueError("Incomplete or duplicate severe results")
    for r in rows.itertuples():
        if (r.false_rejects_triplet - r.false_rejects_l1 != r.genuine_harms - r.genuine_recoveries
                or r.false_accepts_triplet - r.false_accepts_l1
                != r.newly_accepted_impostors - r.newly_rejected_impostors):
            raise ValueError(f"Paired count mismatch: {r.db}")
        for method, suffix in zip(METHODS, ("l1", "triplet")):
            metric = metrics.loc[r.dataset, r.db, method]
            np.testing.assert_allclose(
                [getattr(r, f"false_rejects_{suffix}") / r.genuine_attempts,
                 getattr(r, f"false_accepts_{suffix}") / r.impostor_attempts],
                [metric.attempt_frr, metric.attempt_far], rtol=0, atol=1e-14)
    return rows


def bootstrap(decisions, counts, draws=5000, seed=481):
    """Resample scoped finger IDs within each fixed DB, shared across both roles."""
    rng = np.random.default_rng(seed)
    macro = np.zeros((draws, 2))
    point = np.zeros(2)
    records = []
    if set(zip(decisions.dataset, decisions.db)) != set(zip(counts.dataset, counts.db)):
        raise ValueError("Missing or unexpected databases in scores")
    for r in counts.sort_values(["dataset", "db"]).itertuples():
        frame = decisions[(decisions.dataset == r.dataset) & (decisions.db == r.db)]
        fingers = pd.Index(sorted(frame["gallery_identity"].unique()))
        p = fingers.get_indexer(frame["probe_identity"])
        g = fingers.get_indexer(frame["gallery_identity"])
        genuine = frame["label"].to_numpy(dtype=bool)
        old = frame["accept_0"].to_numpy(dtype=int)
        new = frame["accept_1"].to_numpy(dtype=int)
        if (p < 0).any() or (g < 0).any() or len(frame) != r.genuine_attempts + r.impostor_attempts:
            raise ValueError(f"Invalid pair coverage: {r.db}")
        delta = new - old
        n = len(fingers)
        g_den = np.bincount(p[genuine], minlength=n)
        g_num = np.bincount(p[genuine], weights=-delta[genuine], minlength=n)
        i_den = np.zeros((n, n))
        i_num = np.zeros((n, n))
        np.add.at(i_den, (p[~genuine], g[~genuine]), 1)
        np.add.at(i_num, (p[~genuine], g[~genuine]), delta[~genuine])
        actual = ((1-old[genuine]).sum(), (1-new[genuine]).sum(), old[~genuine].sum(), new[~genuine].sum())
        expected = (r.false_rejects_l1, r.false_rejects_triplet, r.false_accepts_l1, r.false_accepts_triplet)
        if actual != expected or (g_den.sum(), i_den.sum()) != (r.genuine_attempts, r.impostor_attempts):
            raise ValueError(f"Score decisions do not reproduce the saved counts: {r.db}")
        weights = rng.multinomial(n, np.full(n, 1 / n), size=draws)
        def quad(matrix):
            return np.einsum("bi,ij,bj->b", weights, matrix, weights, optimize=True)

        den = quad(i_den)
        if (den == 0).any() or (weights @ g_den == 0).any():
            raise ValueError("Bootstrap draw has no eligible pairs")
        samples = np.column_stack(((weights @ g_num) / (weights @ g_den), quad(i_num) / den))
        estimate = np.array([g_num.sum() / g_den.sum(), i_num.sum() / i_den.sum()])
        macro += samples / len(counts)
        point += estimate / len(counts)
        records.extend(interval_rows(f"{r.dataset}/{r.db}", estimate, samples))
    return pd.DataFrame(records + interval_rows("Macro", point, macro))


def interval_rows(scope, point, samples):
    return [dict(scope=scope, metric=metric, delta_pp=100 * point[i],
                 lo_pp=100 * np.quantile(samples[:, i], .025), hi_pp=100 * np.quantile(samples[:, i], .975))
            for i, metric in enumerate(("FRR", "FAR"))]


def export_private_cases(archive_path, destination, condition_input, models, helpers):
    """Run in the existing Notebook 45 runtime; reproduce only two saved cases."""
    from PIL import Image

    def png(image):
        buffer = io.BytesIO()
        Image.fromarray(helpers.quantize(image)).save(buffer, format="PNG", dpi=(500, 500))
        return buffer.getvalue()

    def verify(data, expected, description):
        if hashlib.sha256(data).hexdigest() != expected:
            raise ValueError(f"Replay differs: {description}")

    with ZipFile(archive_path) as archive:
        report = Report(archive)
        config = json.loads(report.checked("configuration.json", report.marker["configuration_sha256"]))
        if config["split"] != "test_external" or helpers.evaluation_sha != report.marker["configuration_sha256"]:
            raise ValueError("Use the original completed Notebook 45 runtime")
        decisions = report.decisions()
        genuine = decisions[decisions.label.eq(1) & decisions[["score_0", "score_1"]].notna().all(axis=1)]
        chosen = {
            "recovered": genuine[~genuine.accept_0 & genuine.accept_1].iloc[0],
            "harmed": genuine[genuine.accept_0 & ~genuine.accept_1].iloc[0],
        }
        extracts = [report.severe_variant(m, "extraction.csv").set_index("relative_path", verify_integrity=True)
                    for m in METHODS]
        gallery = report.summary("gallery_extraction.csv").set_index("relative_path", verify_integrity=True)
        payloads = {}
        for case, pair in chosen.items():
            records = [table.loc[pair.probe_path] for table in extracts]
            source = helpers.DATA_ROOT / pair.probe_path
            for record in records:
                verify(source.read_bytes(), record.sha256, f"{case}/source probe")
            reference, degraded = condition_input(
                dict(records[0], relative_path=pair.probe_path), "dry_like", "severe")
            for name, image in (("reference", reference), ("probe", degraded)):
                payloads[case, name] = png(image)
            gallery_row = gallery.loc[pair.gallery_path]
            verify((helpers.DATA_ROOT / pair.gallery_path).read_bytes(), gallery_row.sha256, f"{case}/source gallery")
            gallery_reference, _ = condition_input(
                dict(gallery_row, relative_path=pair.gallery_path), "identity", "none")
            payloads[case, "gallery"] = png(gallery_reference)
            verify(payloads[case, "gallery"], gallery_row.png_sha256, f"{case}/gallery")
            original_model = helpers.model
            try:
                for method, record in zip(METHODS, records):
                    helpers.model = models[method]
                    data = png(helpers.restore_image(degraded))
                    verify(data, record.png_sha256, f"{case}/{method}")
                    payloads[case, method] = data
            finally:
                helpers.model = original_model
    destination.mkdir(parents=True, exist_ok=False)
    for (case, name), data in payloads.items():
        (destination / f"{case}_{name}.png").write_bytes(data)
    pd.DataFrame.from_dict(chosen, orient="index").rename_axis("case").to_csv(destination / "cases.csv")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("archive", type=Path)
    parser.add_argument("--bootstrap", action="store_true", help="Requires both severe score CSVs")
    parser.add_argument("--private-decisions", type=Path, help="Local output only; contains biometric pair data")
    args = parser.parse_args()
    with ZipFile(args.archive) as archive:
        report = Report(archive)
        counts = severe_counts(report)
        print(counts.to_string(index=False))
        if args.bootstrap or args.private_decisions:
            decisions = report.decisions()
            print(bootstrap(decisions, counts).to_string(index=False, float_format=lambda x: f"{x:.4f}"))
            if args.private_decisions:
                decisions.to_csv(args.private_decisions, index=False, mode="x")


if __name__ == "__main__":
    main()
