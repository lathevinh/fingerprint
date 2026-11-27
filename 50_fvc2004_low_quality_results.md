# FVC2004: Triplet ở cùng FAR trên ảnh thu thật chất lượng thấp

**Ở FAR 0,1%, lợi thế của L1 + triplet so với L1 rõ hơn khi lọc xuống nhóm điểm NFIQ 2 thấp nhất.** Chênh lệch FRR chuyển từ **+0,44** điểm phần trăm ở nhóm 20% sang **−0,86** ở nhóm 10% và **−1,62** ở nhóm 5%. Trong nhóm 5%, FRR tại mức FAR này là **66,40% với L1** và **64,78% với L1 + triplet**.

| Nhóm NFIQ 2 thấp nhất | Probe | FAR 0,1% | FAR 0,2% | FAR 0,4% | FAR 1,0% |
|---|---:|---:|---:|---:|---:|
| 20% | 306 | +0,44 | −0,13 | +0,68 | −0,08 |
| 10% | 153 | **−0,86** | −1,02 | +0,11 | −0,68 |
| 5% | 77 | **−1,62** | −0,59 | +0,54 | +2,02 |

Mỗi ô là **FRR của L1 + triplet trừ FRR của L1**, tính bằng điểm phần trăm; số âm có lợi cho triplet. Các nhóm lồng nhau, xếp theo NFIQ 2 của ảnh gốc trong từng DB quang học FVC2004 (DB1/DB2), không dùng simulator. FAR và FRR lấy trung bình đều theo hai DB; FRR tại cùng FAR được nội suy từ các điểm vận hành thực nghiệm.

Đây là **tín hiệu ở vùng FAR thấp**, không phải cải thiện ở mọi điểm vận hành: tại FAR 0,4%, triplet có FRR cao hơn L1 ở cả ba nhóm. Phân tích mang tính thăm dò, đặc biệt với 77 probe ở nhóm 5%; không dùng để chốt lại ngưỡng hay thay thế kết luận của phép thử chính.
