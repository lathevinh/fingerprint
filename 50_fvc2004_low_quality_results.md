# FVC2004: Đối chứng phục hồi ở cùng FAR

## Toàn bộ tập test: raw, L1 và L1 + triplet

**Ở FAR 0,1%, trên suy giảm nặng mô phỏng, L1 + triplet giảm FRR macro 21,39 điểm phần trăm so với raw và 4,60 điểm so với L1.** Đây là hai đối chứng khác nhau: so với raw đo lợi ích của cả pipeline phục hồi; so với L1 đo phần đóng góp thêm của triplet.

Ba nhánh dùng chung cặp probe–gallery và matcher NBIS trên FVC2004 DB1–DB3 (2.310 probe, 330 gallery). Raw là probe đầu vào không phục hồi: ở ba điều kiện mô phỏng, raw vẫn chịu đúng cùng suy giảm như hai nhánh còn lại. Macro lấy trung bình đều theo DB tại cùng một ngưỡng cho mỗi phương pháp rồi nội suy FRR tại FAR đích; mỗi hàng theo DB dùng đường cong riêng của DB đó. Chênh lệch dưới đây là **triplet trừ đối chứng**, tính bằng điểm phần trăm, với khoảng tin cậy percentile 95% từ 2.000 lượt bootstrap ghép cặp theo ngón trong từng DB, tính lại điểm vận hành ở mỗi lượt. Khoảng tin cậy không hiệu chỉnh đa so sánh.

### Macro tại FAR 0,1%

| Điều kiện | FRR raw | FRR L1 | FRR L1 + triplet | Δ so với raw [KTC 95%] | Δ so với L1 [KTC 95%] |
|---|---:|---:|---:|---:|---:|
| Ảnh gốc | 23,451% | 23,771% | 23,479% | +0,028 [−0,630; +1,176] | −0,292 [−1,116; +0,673] |
| Nhẹ mô phỏng | 25,884% | 24,940% | 25,366% | −0,518 [−1,879; +0,654] | +0,426 [−0,898; +1,482] |
| Vừa mô phỏng | 31,012% | 26,103% | 25,763% | **−5,249 [−7,127; −3,639]** | −0,340 [−1,457; +0,857] |
| Nặng mô phỏng | 64,095% | 47,308% | 42,704% | **−21,391 [−24,141; −18,318]** | **−4,604 [−6,603; −2,741]** |

### Mức nặng theo DB tại FAR 0,1%

| DB | FRR raw | FRR L1 | FRR L1 + triplet | Δ so với raw [KTC 95%] | Δ so với L1 [KTC 95%] |
|---|---:|---:|---:|---:|---:|
| DB1 | 58,770% | 45,988% | 44,261% | −14,509 [−17,756; −11,011] | −1,726 [−4,156; +0,761] |
| DB2 | 72,699% | 55,814% | 50,830% | −21,869 [−26,473; −17,262] | −4,984 [−7,557; −1,665] |
| DB3 | 57,253% | 39,334% | 32,974% | −24,279 [−29,925; −18,564] | −6,359 [−9,482; −2,241] |

Ở mức vừa, pipeline triplet hơn raw ở mức macro, nhưng lợi ích riêng của triplet so với L1 chưa rõ. Ở mức nặng, hai chênh lệch macro đều có khoảng tin cậy nằm dưới 0; so với L1 riêng ở DB1, khoảng vẫn chứa 0. Với ảnh gốc và mức nhẹ, chưa có lợi thế macro rõ ràng. Đây là phân tích hồi cứu trên test tại một mốc FAR, không phải hiệu chỉnh ngưỡng triển khai hay xác nhận hiệu quả trên vân tay khô thật.

## Ảnh thu thật chất lượng thấp theo NFIQ 2

**Ở FAR 0,1%, triplet giảm FRR ở nhóm 5% và 10% điểm NFIQ 2 thấp nhất, nhưng không giảm ở nhóm 20%.** Khi mở rộng từ 5% lên 10% rồi 20%, tức là đưa thêm ảnh xếp hạng chất lượng cao hơn vào từng DB, mức giảm FRR thu hẹp từ **1,62** xuống **0,86 điểm phần trăm**, rồi đảo chiều thành **tăng 0,44 điểm phần trăm**.

| Nhóm NFIQ 2 thấp nhất | Probe | FRR tại FAR 0,1%: L1 → L1 + triplet | ΔFRR tại FAR 0,1% | ΔFRR tại FAR 0,2% | ΔFRR tại FAR 0,4% | ΔFRR tại FAR 1,0% |
|---|---:|---:|---:|---:|---:|---:|
| 5% | 77 | 66,397% → 64,777% | **−1,62** | −0,59 | +0,54 | +2,02 |
| 10% | 153 | 54,524% → 53,665% | **−0,86** | −1,02 | +0,11 | −0,68 |
| 20% | 306 | 42,134% → 42,576% | +0,44 | −0,13 | +0,68 | −0,08 |

**ΔFRR = FRR của L1 + triplet trừ FRR của L1**, tính bằng điểm phần trăm; số âm có lợi cho triplet. Các nhóm lồng nhau, xếp theo NFIQ 2 của ảnh gốc trong từng DB quang học FVC2004 (DB1/DB2), không dùng simulator. FAR và FRR lấy trung bình đều theo hai DB; FRR tại cùng FAR được nội suy từ các điểm vận hành thực nghiệm.

Đây là **tín hiệu thăm dò ở FAR 0,1%**, không chứng minh rằng triplet chỉ có ích với ảnh chất lượng thấp hay rằng hiệu quả giảm đều ở mọi FAR. Ví dụ, tại FAR 0,4%, triplet có FRR cao hơn L1 ở cả ba nhóm. Các nhóm lồng nhau không phải ba phép xác nhận độc lập; riêng nhóm 5% chỉ có 77 probe.
