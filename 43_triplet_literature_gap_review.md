# Đối chiếu literature: đóng góp của thí nghiệm L1–triplet

Rà soát có mục tiêu ngày 27/11/2026, không phải systematic review. Chọn
sáu công trình theo độ liên quan đến phục hồi, vân tay khô, DMD và cách
báo cáo lỗi xác minh; không khẳng định đây là sáu bài mới nhất.

| Công trình | Dữ liệu và đối chứng | Đo gì? | Hàm ý cho bài này |
|---|---|---|---|
| [Ojha & Kumar, Fingerprint Restoration and Identification using Pix2Pix cGAN and Triplet Loss (IEEE ICWITE, 2024)](https://doi.org/10.1109/ICWITE59797.2024.10503554) | Phần III và Hình 3 mô tả Pix2Pix phục hồi, sau đó mạng Siamese học embedding bằng triplet loss với khoảng cách Euclid. Bài không nêu triplet loss truyền gradient về generator. SOCOFing chia 70/15/15, nhưng không nêu rõ tách theo người hay theo ngón. | Hình 5: **80%** trên 60 cặp cùng/khác ngón của SOCOFing, là xác minh nhị phân, không phải rank-1. Bảng II: **86%** trên FVC2000 DB1 B. Không thấy mô tả đủ rõ về cách khóa ngưỡng để đối chiếu trực tiếp. | Tiền lệ cho việc dùng triplet trong pipeline phục hồi–nhận dạng. Khác biệt có thể mô tả là triplet cập nhật trực tiếp bộ phục hồi trong nghiên cứu này. Không dùng 80% hoặc 86% làm baseline trực tiếp và không tuyên bố lần đầu. |
| [Two-stage quality adaptive fingerprint image enhancement (2019)](https://www.sciencedirect.com/science/article/pii/S0262885619300150) ([tóm tắt bổ sung](https://www.bohrium.com/paper-details/two-stage-quality-adaptive-fingerprint-image-enhancement-using-fuzzy-c-means-clustering-based-fingerprint-quality-analysis/812794620290269184-2657)) | FVC2002/FVC2004, phân nhóm chất lượng có khô/ướt; so tiền xử lý thích ứng ghép với Gabor, STFT hoặc ODF với các cách tăng cường hiện có. | EER với NBIS và VeriFinger. Chưa xác minh quy tắc khóa ngưỡng từ toàn văn. | Tăng cường theo chất lượng và dùng NBIS trên FVC đã có tiền lệ. Gabor là đối chứng phù hợp hơn việc chỉ so hai loss học sâu. |
| [Cheng et al., MTS + CCRGAN (IEEE, 2023)](https://ieeexplore.ieee.org/document/10213986) ([bản toàn văn](https://www.researchgate.net/publication/373034819_Multiple_Training_Stage_Image_Enhancement_Enrolled_with_CCRGAN_Pseudo_Templates_for_Large_Area_Dry_Fingerprint_Recognition/fulltext/64d4da37c80b930269045157/Multiple-Training-Stage-Image-Enhancement-Enrolled-with-CCRGAN-Pseudo-Templates-for-Large-Area-Dry-Fingerprint-Recognition.pdf)) | FVC2002/FVC2004; thành phần CCRGAN dùng dữ liệu huấn luyện riêng. So với các phương pháp đã công bố, có VeriFinger trong bảng benchmark; có nhánh dùng mẫu đăng ký tổng hợp. | EER theo DB là kết quả chính trong bảng đối chiếu; đó không phải FRR/FAR đo trên test ở ngưỡng đã khóa từ validation. | Đối thủ gần nhất về bài toán vân tay khô. Không thể mượn EER của họ làm baseline trực tiếp; dữ liệu, gallery và điểm vận hành khác nhau. |
| [Finger-UNet (2023, preprint)](https://ar5iv.labs.arxiv.org/html/2310.00629) | SFinGe cho phục hồi có ảnh đích; FVC2002 và NIST SD302 cho đánh giá. So ảnh gốc và các phương pháp Hong, Joshi; dùng L1 với nhánh phụ minutiae/hướng ridge. | SSIM/RMSE/PSNR, NFIQ2; mục matching dùng MINDTCT/BOZORTH3 và so **điểm genuine trung bình** theo DB của FVC2002. Không có FAR/FRR theo ngưỡng trong bảng matching đó. | So đánh giá rất gần: cùng matcher và có FVC2002, nhưng điểm genuine tốt hơn không cho biết impostor có bị nhận nhầm nhiều hơn không. L1 và giám sát đặc trưng vân tay cũng không tự thân là mới. |
| [Pan et al., Minutiae-Anchored Local Dense Representation (2025, preprint)](https://arxiv.org/html/2507.15297v1) | Nhiều dạng ảnh, gồm rolled, plain, partial, contactless và latent; so với matcher như VeriFinger và các biến thể DMD. | Rank-1, TAR tại FAR thấp và DET, tùy bài toán. | DMD là kỹ thuật kế thừa và đánh giá tại FAR thấp đã có. Điểm cần phân biệt là dùng DMD làm tín hiệu huấn luyện **ảnh phục hồi**, sau đó chấm bằng NBIS, không phải đề xuất bộ mô tả DMD hay matcher mới. |
| [Beyond ROC-AUC: Operating-Point Performance Reporting for Biometric Verification (2026, preprint)](https://arxiv.org/html/2606.20680v1) | So bảy matcher đã huấn luyện trên nhiều loại sinh trắc, gồm FVC2002 Set B; không phải thí nghiệm phục hồi vân tay khô. | Chỉ số ở điểm vận hành, khoảng tin cậy, phân tích bootstrap theo cặp; nhấn mạnh giới hạn số lượt impostor. | Không thể tuyên bố ý tưởng đo ở điểm vận hành hay tránh che khuất đánh đổi là mới. Bài này phải đóng góp bằng thiết kế đối chứng và bằng chứng riêng cho phục hồi. |

## Luận điểm có thể bảo vệ

**Xác minh mã huấn luyện.** Trong [Notebook 39](./39_native_triplet_replication_training.ipynb#L950),
nhánh phụ phạt `max(0, 0.2 + điểm impostor cao nhất − điểm genuine)`.
Gradient đi qua điểm so khớp DMD về ảnh phục hồi rồi về tham số U-Net.
Adam cập nhật U-Net bằng `∇L1 + 0.1 × ∇triplet`; DMD không được cập nhật.
NBIS đánh giá đầu ra, không cung cấp gradient huấn luyện. Đối chứng
thực tế là **U-Net L1 so với cùng U-Net L1 + triplet**, không phải
Pix2Pix gốc so với Pix2Pix + triplet và cũng không so trực tiếp với Ojha
& Kumar. Hai nhánh dùng chung khởi tạo và ngân sách hai epoch; cùng quy
tắc chọn theo MAE validation cho checkpoint epoch 1 (L1) và epoch 2
(triplet), nên đây là so sánh hai pipeline có chọn checkpoint, không phải
so sánh hai checkpoint cùng epoch.

**Câu hỏi:** Khi chỉ bổ sung tín hiệu triplet vào bộ phục hồi L1, khác
biệt trên ảnh hỏng nặng mô phỏng có còn trên các ngón giữ lại, ở ngưỡng
đã chọn từ validation, mà không làm tăng nhận nhầm ở bất kỳ DB nào?

[Thí nghiệm giữ lại](./41_triplet_heldout_results.md) cho câu trả lời
hai phần: FRR trung bình đều sáu DB giảm từ **37,76% xuống 33,57%**,
FAR trung bình từ **0,184% xuống 0,076%**, nhưng **không đạt**
[tiêu chí định trước](./41_triplet_heldout_test_protocol.md). Ở
FVC2000/DB2, nhận nhầm tăng từ **3 lên 4 trên 1.904 lượt**. Đây là ví dụ
cụ thể về kết luận từ trung bình khác kết luận theo từng DB. Một lượt
tăng đủ để trượt quy tắc thực nghiệm; **không** đủ để khẳng định FAR
tổng thể của DB đó tăng có ý nghĩa thống kê. Hai seed lặp tín hiệu trên
validation, không phải hai lần xác nhận trên test.

Trong phần tài liệu truy cập được, chưa xác minh thấy cùng tổ hợp: đối chứng
L1–L1+triplet trên ảnh FVC suy giảm có kiểm soát, chấm bằng matcher khác
với tín hiệu huấn luyện, khóa ngưỡng trước khi mở tập giữ lại và công bố
cả thay đổi quyết định theo cặp lẫn điều kiện FAR theo từng DB. Đây là
**khoảng trống hẹp để viết bản thảo thực nghiệm**, không phải bằng chứng
chưa từng có nghiên cứu tương tự hoặc phương pháp vượt SOTA. Đối chiếu
với toàn văn Ojha & Kumar do người dùng cung cấp chỉ xác lập khác biệt
với pipeline **được mô tả** trong bài đó; không suy ra tính mới trên
toàn bộ literature.

## Đối chứng raw và Gabor trên validation

Các báo cáo đã lưu của [Notebook 16](./16_gabor_validation_matching.ipynb),
[Notebook 38](./38_native_counterfactual_nbis_validation.ipynb) và
[Notebook 40](./40_native_triplet_replication_validation.ipynb) dùng cùng
split validation, 938 probe, 134 gallery gốc và 21.518 cặp mỗi điều kiện.
Mã kiểm tra cùng cấu hình cặp, simulator và binary NBIS theo báo cáo gốc
của [Notebook 14](./14_structure_validation_matching.ipynb). Notebook 16
tái tính ngưỡng theo đúng công thức và điểm raw ảnh gốc của Notebook 14;
Notebook 38/40 đọc ngưỡng đã lưu của Notebook 14. Tất cả dùng ngưỡng
cố định theo DB, vẫn tính cặp không so được là từ chối, không cân FAR
riêng cho từng phương pháp. Đối chiếu này dựa trên mã và output lưu
trong notebook, không tái kiểm tra từng CSV điểm thô của Gabor.

| Phương pháp | Nguồn | FRR (%) | FAR (%) |
|---|---|---:|---:|
| Raw: ảnh suy giảm, không phục hồi | Notebook 38; khớp Notebook 16 ở độ chính xác hiển thị | 32,142 | 0,368 |
| Gabor | Notebook 16 | 38,905 | 0,564 |
| U-Net L1, seed gốc | Notebook 38 | 19,758 | 0,584 |
| U-Net L1 + triplet, seed gốc | Notebook 38 | 18,121 | 0,603 |
| U-Net L1, seed lặp | Notebook 40 | 20,491 | 0,601 |
| U-Net L1 + triplet, seed lặp | Notebook 40 | 18,571 | 0,629 |

Trung bình đều sáu DB và ba mức `dry_like`, gồm mọi lượt thử, không
gồm ảnh gốc. Ở điểm vận hành này, cả hai seed U-Net đều giảm FRR so với
raw nhưng tăng FAR. Riêng mức nặng trong Notebook 38, triplet so với raw
giảm FRR **29,28 điểm phần trăm** và tăng FAR **0,290 điểm phần trăm**.
Cấu hình Gabor đã thử kém raw ở cả hai tỷ lệ trung bình, không suy rộng
cho mọi biến thể Gabor. Đây là bảng bổ sung trên validation; không dùng
để thay đổi kết luận trên tập giữ lại.

### Khi nào đánh đổi này đáng chấp nhận?

So với raw, L1 + triplet ở seed gốc giảm FRR **14,02 điểm phần trăm**
trung bình ba mức và **29,28 điểm phần trăm** ở mức nặng; FAR tăng tương
ứng **0,235** và **0,290 điểm phần trăm**. Quy đổi từ tỷ lệ trung bình
ba mức, với 10.000 lượt cùng ngón và 10.000 lượt khác ngón, đó là khoảng
**1.402 lượt từ chối nhầm tránh được** đổi lấy **24 lượt chấp nhận nhầm
thêm**. Đây là ví dụ chuẩn hóa, không phải số lượt quan sát hay tỷ lệ
lượt thật/giả trong triển khai.

Nếu ứng dụng có trần FAR bắt buộc, phải đạt trần đó trước khi cân nhắc
lợi ích FRR. Nếu cho phép đánh đổi, so **số lượt từ chối nhầm tránh được
× chi phí mỗi lượt** với **số lượt chấp nhận nhầm tăng thêm × chi phí mỗi
lượt** theo lưu lượng thực tế. Với số lượt hai loại bằng nhau, điểm hòa
vốn minh họa là khoảng **60:1** về chi phí một lần chấp nhận nhầm so
với một lần từ chối nhầm (khoảng **101:1** ở mức nặng). Vì thế, số liệu
ủng hộ lợi ích giảm từ chối nhầm, nhưng không đủ để kết luận đánh đổi
đáng chấp nhận cho mọi ứng dụng. So với raw ở đây là hiệu quả của cả
pipeline phục hồi, không phải lợi ích riêng của triplet.

Trên test giữ lại, so sánh là **triplet với L1**, không phải với raw.
Cả FRR và FAR trung bình đều giảm ở mức nặng, nhưng một DB tăng FAR và
vượt tiêu chí định trước. Không dùng phân tích chi phí trên validation
để đổi kết luận test.

## Xác nhận ngoài trên FVC2004

[Notebook 45](./45_fvc2004_external_nbis_test.ipynb) **đạt** [tiêu chí
đã khóa](./45_fvc2004_external_protocol.md) ở mức hỏng nặng mô phỏng.
Đối chiếu CSV với `completion.json`, hash giao thức và số lượt đổi
quyết định theo cặp. Ngưỡng chuyển từ validation là 20 (L1) và 22
(triplet), không cân lại trên FVC2004.

| DB | Từ chối nhầm L1 → triplet (/770) | Chấp nhận nhầm L1 → triplet (/83.930) |
|---|---:|---:|
| DB1 | 312 → 308 (−4) | 290 → 191 (−99) |
| DB2 | 395 → 385 (−10) | 178 → 112 (−66) |
| DB3 | 185 → 186 (+1) | 786 → 410 (−376) |
| Tổng | 892 → 879 (−13) | 1.254 → 713 (−541) |

Ở mức nặng, FRR trung bình giảm **38,61% → 38,05%** và FAR giảm
**0,498% → 0,283%**. DB2 đóng góp phần lớn mức giảm từ chối nhầm;
DB3 đóng góp phần lớn mức giảm chấp nhận nhầm nhưng FRR tăng nhẹ.
Mức giảm ròng gồm 135 cặp cùng ngón được chấp nhận thêm và 122 cặp
bị từ chối thêm; 902 cặp khác ngón được chặn thêm nhưng 361 cặp khác
lại được chấp nhận. Kết quả mức nặng không đổi khi loại trùng byte.

Kết quả bổ sung bằng chứng trên bộ dữ liệu khác dưới cùng cơ chế mô
phỏng. Nó không đảo ngược FAIL trên FVC2000/2002 hay chứng minh lợi
ích ở mọi điều kiện: với ảnh gốc và hai mức nhẹ hơn trên FVC2004,
FAR giảm nhưng FRR tăng. Không suy diễn ý nghĩa thống kê từ quy tắc
đạt/trượt; các cặp so khớp dùng chung probe hoặc gallery.

## Quyết định trước khi nhắm Q3

**Viết được bản thảo; chưa nên nộp dưới dạng bài đề xuất mô hình vượt
baseline.** Reviewer có thể yêu cầu đối chứng mạnh hơn, độ bất định có
tính đến các cặp dùng chung probe/gallery, và bằng chứng ngoài mô phỏng.
Hiện chỉ có một matcher đánh giá chính và chưa có dữ liệu vân tay khô
thực tế có nhãn.

**Bước tiếp theo, không train hay mở lại test:** viết bản thảo với
bảng đối chứng validation và kết quả giữ lại tách riêng.
Nếu phải đầu tư thêm một thí nghiệm xác nhận,
ưu tiên một tập **mới** có điều kiện khô thực tế đã ghi nhận, với đối chứng
và protocol khóa trước. Không đổi ngưỡng rồi chạy lại tập giữ lại hiện tại.
