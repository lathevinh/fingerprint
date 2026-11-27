# FVC2004: Triplet ở cùng FAR trên ảnh thu thật chất lượng thấp

**Ở FAR 0,1%, triplet giảm FRR ở nhóm 5% và 10% điểm NFIQ 2 thấp nhất, nhưng không giảm ở nhóm 20%.** Khi mở rộng từ 5% lên 10% rồi 20%, tức là đưa thêm ảnh xếp hạng chất lượng cao hơn vào từng DB, mức giảm FRR thu hẹp từ **1,62** xuống **0,86 điểm phần trăm**, rồi đảo chiều thành **tăng 0,44 điểm phần trăm**.

| Nhóm NFIQ 2 thấp nhất | Probe | FRR tại FAR 0,1%: L1 → L1 + triplet | ΔFRR tại FAR 0,1% | ΔFRR tại FAR 0,2% | ΔFRR tại FAR 0,4% | ΔFRR tại FAR 1,0% |
|---|---:|---:|---:|---:|---:|---:|
| 5% | 77 | 66,397% → 64,777% | **−1,62** | −0,59 | +0,54 | +2,02 |
| 10% | 153 | 54,524% → 53,665% | **−0,86** | −1,02 | +0,11 | −0,68 |
| 20% | 306 | 42,134% → 42,576% | +0,44 | −0,13 | +0,68 | −0,08 |

**ΔFRR = FRR của L1 + triplet trừ FRR của L1**, tính bằng điểm phần trăm; số âm có lợi cho triplet. Các nhóm lồng nhau, xếp theo NFIQ 2 của ảnh gốc trong từng DB quang học FVC2004 (DB1/DB2), không dùng simulator. FAR và FRR lấy trung bình đều theo hai DB; FRR tại cùng FAR được nội suy từ các điểm vận hành thực nghiệm.

Đây là **tín hiệu thăm dò ở FAR 0,1%**, không chứng minh rằng triplet chỉ có ích với ảnh chất lượng thấp hay rằng hiệu quả giảm đều ở mọi FAR. Ví dụ, tại FAR 0,4%, triplet có FRR cao hơn L1 ở cả ba nhóm. Các nhóm lồng nhau không phải ba phép xác nhận độc lập; riêng nhóm 5% chỉ có 77 probe.
