# Protocol khóa trước: L1 so với triplet trên tập giữ lại

**Phiên bản 1 — 27/11/2026 (+07:00).** Đây là protocol, không phải kết quả
test. Không đọc ảnh, tạo điểm hay chạy đánh giá test khi khóa bản này.

## 1. Mô hình và ngưỡng đã khóa

Chỉ dùng hai checkpoint `selected.pt` mà Notebook 40 đã đánh giá từ lần
huấn luyện seed `20261127`: `native_l1` (epoch 1) và `native_triplet`
(epoch 2). Không thay bằng seed cũ, checkpoint khác hoặc ensemble.

- Báo cáo Notebook 40:
  `evaluations/native_triplet_replication_validation_v1/b1ddff0a86f722ea0663`.
- SHA-256 `configuration.json` của Notebook 40:
  `b1ddff0a86f722ea06634f784050b6d8cfb6a0e37a0a91f010acc499df6e4127`.
- SHA-256 cấu hình train Notebook 39:
  `59ad0c66eee00fe6e050cb02749083cc39ebb7af7a31a599a450c94d4e4a7d16`.
- Trước khi đọc ảnh test, xác minh cấu hình Notebook 40 theo hash trên.
  Lấy hai mục `model_checkpoints` từ chính cấu hình đó; kiểm tra hash của
  `selected.pt`, tên nhánh và epoch theo các mục này. Dùng các thư mục theo
  hash, không lấy checkpoint từ con trỏ `latest` hay từ kết quả test.
- Ngưỡng dưới đây lấy từ phân tích `dry_like/severe` trên **validation**:
  với mỗi DB, đặt trần bằng số lượt nhận nhầm của L1 tại ngưỡng gốc;
  cho mỗi mô hình chọn ngưỡng nguyên không âm nhỏ nhất thỏa trần đó.
  Không chia các điểm đồng hạng. SHA-256 CSV nguồn:
  `453d2eb0ab533147561a52dcb9de5b6d80f568bcc7f14a782388f3513967ab06`.

| Bộ dữ liệu | DB | Ngưỡng L1 | Ngưỡng triplet |
|---|---|---:|---:|
| FVC2000 | DB1 | 22 | 22 |
| FVC2000 | DB2 | 19 | 20 |
| FVC2000 | DB3 | 16 | 17 |
| FVC2002 | DB1 | 23 | 24 |
| FVC2002 | DB2 | 20 | 22 |
| FVC2002 | DB3 | 20 | 30 |

Dùng cùng bảng ngưỡng này cho mọi điều kiện báo cáo. Không cân lại FAR,
không quét ngưỡng trên test. Trần validation chỉ dùng để chọn ngưỡng;
không giả định FAR thực đo trên test sẽ bằng nhau.

## 2. Tập test và phép đo

- Chỉ dùng split `test_synthetic` đã khóa ở Notebook 03: FVC2000 và
  FVC2002, DB1–DB3. Xác minh hash file và split protocol theo cấu hình
  Notebook 40. Không dùng `train`, `validation`, `quarantine` hoặc
  `test_external` (FVC2004) làm probe hay gallery.
- Tạo cặp bằng quy tắc Notebook 05 trên split riêng này: impression 1
  là gallery gốc; impressions 2–8 là probe; mỗi probe so với mọi gallery
  trong cùng DB, hướng probe → gallery. Một cặp cùng ngón là genuine,
  còn lại là impostor. Kỳ vọng: **145 gallery, 1.015 probe, 1.015 cặp
  genuine và 24.388 cặp impostor** mỗi điều kiện, tính từ số ngón đã khóa.
- Điều kiện chính: `dry_like/severe`. Điều kiện phụ: `identity/none`,
  `dry_like/mild`, `dry_like/moderate`. Giữ nguyên simulator, quy tắc
  seed theo đường dẫn, DPI và quy trình gốc của Notebook 40. Cùng một
  probe suy giảm cho hai mô hình. Giữ nguyên gallery gốc; suy luận ảnh
  toàn khổ FP32, round-to-uint8 PNG 500 DPI, MINDTCT và BOZORTH3 với cùng
  bản NBIS và cờ đã khóa. Xác minh hash simulator và binary theo cấu
  hình Notebook 40 trước khi chạy.
- Chấp nhận khi cặp có điểm hợp lệ và `score >= threshold`. Cặp không
  match được tính là từ chối, không bị loại khỏi mẫu số FRR/FAR.
  Tính FRR và FAR từ mọi lượt, rồi lấy trung bình đều sáu DB cho
  **từng điều kiện**. Báo cáo thêm số lượt, lượt đổi quyết định theo cặp,
  lượt không match được và phân tích nhạy cảm loại trùng byte theo
  Notebook 05; không dùng phân tích nhạy cảm để thay đổi kết luận chính.

## 3. Quy tắc kết luận trước khi xem test

Kết quả chính **đạt** chỉ khi đồng thời:

1. Trên `dry_like/severe`, FRR trung bình đều sáu DB của triplet **thấp
   hơn nghiêm ngặt** so với L1.
2. Trên `dry_like/severe`, FAR thực đo của triplet **không cao hơn L1 ở
   bất kỳ DB nào**. So bằng tỷ lệ chính xác từ số lượt, không dùng số
   đã làm tròn. Đây là quy tắc nghiên cứu bảo thủ (mức tăng cho phép:
   **0 điểm phần trăm**), không phải chuẩn an toàn triển khai.

Nếu một điều kiện không đạt, ghi **không đạt theo protocol** và giữ L1
làm mặc định. Nếu đạt, kết luận giới hạn ở tập giữ lại và suy giảm nặng
mô phỏng, không tuyên bố hiệu quả trên vân tay khô thực tế, trên mọi
điều kiện hoặc có ý nghĩa thống kê. Báo cáo cả điều kiện phụ dù tốt hay
xấu; không thay mô hình mặc định chỉ dựa vào kết quả này.

Chỉ đánh giá một lần với cấu hình này và lưu đầy đủ kết quả. Sai hash,
thiếu DB, thiếu đầu vào hoặc sai số lượng cặp thì dừng, không xuất kết
luận. Sau khi xem điểm test, không đổi mô hình, ngưỡng, split hay tiêu
chí rồi đánh giá lại trên chính tập đó.
