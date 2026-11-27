# Notebook 41 — Kết quả test giữ lại

Ngày chạy: 27/11/2026. Nguồn: output cuối của
[Notebook 41](./41_triplet_heldout_nbis_test.ipynb).
Đánh giá theo [protocol đã khóa](./41_triplet_heldout_test_protocol.md).
Các số chi tiết bên dưới lấy từ CSV gốc đã đối chiếu SHA-256 với
`completion.json`. Bản tóm tắt này không thay thế các báo cáo gốc.

**Kết luận theo protocol: FAIL. Giữ L1 làm mặc định.**

Ở mức hỏng nặng mô phỏng, `triplet` giảm FRR trung bình chính xác
**4,195529 điểm phần trăm**. FAR trung bình cũng giảm, nhưng FAR
tăng ở **FVC2000/DB2**. Protocol yêu cầu FAR không tăng ở bất kỳ DB nào.

| Điều kiện | FRR L1 (%) | FRR triplet (%) | FAR L1 (%) | FAR triplet (%) |
|---|---:|---:|---:|---:|
| Ảnh gốc | 10,7765 | 13,4883 | 0,7130 | 0,4065 |
| Hỏng nhẹ | 10,1793 | 13,8140 | 0,6589 | 0,3895 |
| Hỏng vừa | 11,7018 | 14,6184 | 0,5984 | 0,2642 |
| Hỏng nặng | 37,7610 | 33,5655 | 0,1836 | 0,0763 |

FRR là tỷ lệ từ chối nhầm; FAR là tỷ lệ chấp nhận nhầm. Bảng dùng
trung bình đều 6 DB, trên mọi lượt thử, theo độ chính xác của output.
Không suy rộng sang vân tay khô thực tế.

## Kết quả và thảo luận

Ở FVC2000/DB2, trong điều kiện hỏng nặng mô phỏng, `triplet` giảm số
lượt từ chối nhầm từ **31 xuống 27 trên 119 lượt đúng** (26,05% xuống
22,69%). Tuy nhiên, số lượt chấp nhận nhầm tăng từ **3 lên 4 trên
1.904 lượt sai**, tức FAR tăng từ **0,158% lên 0,210%** (+0,0525 điểm
phần trăm). Theo đối chiếu từng cặp, `triplet` chấp nhận nhầm thêm 4
lượt mà L1 đã từ chối, đồng thời chặn được 3 lượt mà L1 đã chấp nhận
nhầm. Mức tăng ròng 1 lượt là đủ để không đạt tiêu chí đã khóa.

Vì vậy, mặc dù `triplet` cải thiện đồng thời hai tỷ lệ trung bình trên
ảnh hỏng nặng mô phỏng, lợi ích không đáp ứng yêu cầu FAR theo từng DB.
Trên ảnh gốc và hai mức suy giảm nhẹ hơn, FRR trung bình của `triplet`
cũng cao hơn L1. Giữ L1 làm mặc định; không chỉnh ngưỡng rồi thử lại trên
cùng tập test.

[Notebook 42](./42_save_notebook41_reports.ipynb) đã lưu bốn báo cáo gốc
trên Drive tại `FingerprintResearch/evaluations/native_triplet_heldout_test_v1`:
`completion.json`, `macro_metrics.csv`, `test_metrics.csv` và
`paired_attempt_changes.csv`.
