# Bổ sung minh chứng trước khi nộp

## Bảng 5 — FVC2000/2002, hỏng nặng mô phỏng

Số đếm từ Notebook 41, đã đối chiếu checksum báo cáo và FRR/FAR trong `test_metrics.csv`. Mũi tên là **L1 → L1 + triplet**. Mỗi cặp không so được được tính là từ chối, không bị loại khỏi mẫu số.

| Bộ | DB | Cặp cùng ngón | Từ chối nhầm | Cặp khác ngón | Chấp nhận nhầm |
|---|---|---:|---:|---:|---:|
| FVC2000 | DB1 | 203 | 100 → 69 | 5.684 | 3 → 3 |
| FVC2000 | DB2 | 119 | 31 → 27 | 1.904 | 3 → 4 |
| FVC2000 | DB3 | 203 | 72 → 66 | 5.684 | 13 → 2 |
| FVC2002 | DB1 | 140 | 25 → 28 | 2.660 | 6 → 1 |
| FVC2002 | DB2 | 189 | 36 → 24 | 4.914 | 9 → 6 |
| FVC2002 | DB3 | 161 | 127 → 128 | 3.542 | 9 → 0 |
| **Tổng** | | **1.015** | **391 → 342** | **24.388** | **43 → 16** |

Tổng số lượt không phải macro trung bình đều theo DB. [Kết quả chính](./47_fingerprint_experimental_results.md) vẫn là **FAIL** vì FVC2000/DB2 tăng một lần chấp nhận nhầm.

## Khoảng bất định ghép cặp trên FVC2004

Phân tích bổ sung sau test, chỉ cho điều kiện chính `dry_like/severe`; không quét ngưỡng và không đổi tiêu chí PASS/FAIL. Script xác minh hash các biến thể và tái tạo quyết định từ điểm NBIS ở ngưỡng đã khóa (20/22). Cả hai nhánh dùng cùng mẫu bootstrap.

**Bootstrap theo ngón:** 5.000 lần, seed 481, lấy mẫu ngón có hoàn lại trong từng DB cố định. Cặp cùng ngón mang trọng số số lần ngón xuất hiện; cặp khác ngón mang tích trọng số của ngón probe và ngón gallery. Dùng chung trọng số khi một ngón xuất hiện ở cả hai vai trò; không lấy từng cặp làm quan sát độc lập. Macro tính lại bằng trung bình đều các DB ở mỗi lần lấy mẫu. Báo khoảng percentile 95% theo từng chỉ số, không điều chỉnh đa kiểm định. Khoảng phản ánh bất định lấy mẫu ngón trong các DB này, không bao hàm biến động seed huấn luyện, hiệu chỉnh ngưỡng hay chọn DB.

| Phạm vi | ΔFRR, điểm % [khoảng 95%] | ΔFAR, điểm % [khoảng 95%] |
|---|---:|---:|
| DB1 | −0,5195 [−2,5974; +1,5584] | −0,1180 [−0,2021; −0,0421] |
| DB2 | −1,2987 [−3,7662; +1,1688] | −0,0786 [−0,1466; −0,0204] |
| DB3 | +0,1299 [−2,2078; +2,4675] | −0,4480 [−0,7609; −0,2104] |
| **Macro** | **−0,5628 [−1,9048; +0,7359]** | **−0,2149 [−0,3271; −0,1309]** |

Δ là triplet trừ L1. **Mức giảm FRR macro chưa rõ hướng khi tính bất định**, còn khoảng FAR macro nằm dưới 0 trong phân tích này. PASS theo giao thức không phải kiểm định thống kê.

Tái lập bằng [script audit](./48_fingerprint_submission_audit.py) với Python, NumPy và pandas:

```text
python 48_fingerprint_submission_audit.py NB41.zip
python 48_fingerprint_submission_audit.py NB45.zip --bootstrap
python 48_fingerprint_submission_audit.py NB45.zip --private-decisions LOCAL_PRIVATE.csv
```

Xuất riêng quyết định và điểm từng cặp vào đường dẫn ngoài repo. ZIP hiện có của Notebook 41 chỉ chứa báo cáo tổng hợp, **chưa có điểm theo cặp và chưa tính khoảng tin cậy Notebook 41**. Để bổ sung mà không chạy lại test, cần `configuration.json` và mỗi `completion.json`/`scores.csv` của `dry_like_severe_native_l1` và `dry_like_severe_native_triplet` từ thư mục báo cáo runtime cũ của Notebook 41 (`/content/fingerprint_research/native_pilot_nbis/reports` nếu còn), ghép vào đúng cây ZIP cùng bốn báo cáo đã sao lưu. Script sẽ kiểm tra dấu hoàn thành gốc trước khi đọc điểm.

## Xuất hai ca minh họa riêng tư

Trong **runtime Notebook 45 đã hoàn tất và còn dữ liệu**, đặt script audit và ZIP báo cáo Notebook 45 vào thư mục làm việc của Colab, rồi chạy cell mới bên dưới. Chỉ dựng lại hai probe ở mức nặng: ca cùng ngón từ chối → chấp nhận và ca chấp nhận → từ chối, chọn theo `pair_id` nhỏ nhất trong mỗi nhóm có điểm ở cả hai nhánh. Không chạy lại NBIS. Script kiểm tra SHA-256 ảnh đầu ra L1/triplet và gallery với báo cáo trước khi xuất. Điểm trong `cases.csv` là điểm đã lưu của ảnh phục hồi đối chiếu với **gallery**, không phải với ảnh tham chiếu trước can thiệp.

```python
from importlib import import_module
from pathlib import Path

audit = import_module("48_fingerprint_submission_audit")
audit.export_private_cases(
    Path("/content/NB45.zip"),
    Path("/content/private_fvc2004_cases"),
    condition_input41,
    models,
    active_helpers,
)
```

Mỗi ca xuất ảnh tham chiếu, probe suy giảm, đầu ra L1, đầu ra triplet và gallery, kèm điểm và quyết định hai nhánh. **Chưa có ảnh xuất thật trong workspace local.** Ảnh vân tay và dữ liệu từng cặp không được đưa vào Git.

Hai ca chọn được từ báo cáo gốc đều thuộc FVC2004/DB2: ca phục hồi có điểm **7 → 36**, ca xấu đi **20 → 11** (ngưỡng L1/triplet: **20/22**, chấp nhận nếu điểm ≥ ngưỡng). Đây là ca minh họa theo tiêu chí trên, không đại diện cho tần suất cải thiện.
