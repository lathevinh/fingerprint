# Protocol 45 — xác nhận ngoài trên FVC2004

Khóa trước khi mở ảnh hoặc chấm điểm FVC2004. Notebook 45 kiểm tra
checksum đầu vào và chỉ chạy khi xác nhận `RUN_HELDOUT = True`.

- **Mô hình:** giữ đúng checkpoint Notebook 39 mà Notebook 40 và 41 dùng:
  U-Net L1 epoch 1 và L1 + triplet epoch 2, seed `20261127`. Không train,
  chọn lại checkpoint hoặc thêm nhánh. Notebook kiểm tra hash cấu hình
  39/40, checkpoint, split, simulator và hai binary NBIS.
- **Tập test:** toàn bộ `test_external` của Notebook 03, FVC2004 DB1–DB3,
  gồm cả Set A và B. Mỗi DB có 110 ngón; impression 1 làm gallery gốc,
  impressions 2–8 làm probe. Ghép probe → gallery trong cùng DB: mỗi
  điều kiện có 330 gallery, 2.310 probe, 2.310 cặp cùng ngón và 251.790
  cặp khác ngón. Không đọc ảnh train/validation hoặc test FVC2000/2002.
- **Điều kiện:** ảnh gốc và ba mức `dry_like` từ simulator đã khóa.
  Dùng cùng probe cho hai mô hình. Theo
  [FVC2004](http://bias.csr.unibo.it/fvc2004/databases.asp), DB1/DB2 là
  500 DPI và DB3 là 512 DPI; chuẩn hóa về 500 DPI bằng hàm hiện có.
  Suy luận toàn ảnh FP32; xuất PNG 500 DPI và dùng NBIS
  MINDTCT + BOZORTH3 `-A minminutiae=10`.
- **Ngưỡng chuyển sang tập ngoài:** dùng ngưỡng **20 cho L1, 22 cho
  triplet** ở cả ba DB và mọi điều kiện. Đây là trung vị theo từng mô
  hình của sáu ngưỡng đã chốt từ validation trong
  [protocol 41](./41_triplet_heldout_test_protocol.md). Không ánh xạ theo
  số DB, không quét ngưỡng FVC2004 và không giả định FAR bằng nhau.
- **Báo cáo:** cặp không so được tính là từ chối, không loại khỏi mẫu
  số. Báo FRR/FAR theo DB, trung bình đều ba DB, số lượt đổi quyết định
  theo cặp và độ nhạy loại ảnh trùng byte. Báo tất cả bốn điều kiện.
- **Tiêu chí khóa:** ở mức `dry_like/severe`, triplet chỉ đạt nếu FRR
  macro giảm nghiêm ngặt và FAR không tăng ở bất kỳ DB nào. So tỷ lệ
  chính xác từ số lượt. Đây là tiêu chí nghiên cứu, không phải chuẩn an
  toàn, kiểm định thống kê hay bằng chứng trên da khô thật. Kết quả
  FVC2004 không thay đổi kết luận Notebook 41.

Báo cáo lưu riêng tại
`MyDrive/FingerprintResearch/evaluations/native_triplet_fvc2004_external_v1`.
Không đổi ngưỡng, điều kiện hoặc tiêu chí sau khi xem điểm test.
