# Khung bài báo — Triplet loss cho phục hồi vân tay suy giảm kiểu khô

**Tiêu đề làm việc:** *When Does Triplet-Guided Fingerprint Restoration Improve Verification? A Controlled Study of Simulated Dry-Like Ridge Degradation*

**Luận điểm xuyên suốt:** Thêm tín hiệu so khớp vào bộ phục hồi giúp giảm từ chối nhầm trung bình ở mức hỏng nặng mô phỏng trên hai tập test. Mức lợi không đồng đều: chỉ FVC2004 đạt tiêu chí FAR theo từng DB; ảnh gốc và hai mức nhẹ hơn có đánh đổi ngược lại. Bài nghiên cứu **khi nào cách tiếp cận có ích**, không tuyên bố một mô hình luôn tốt hơn L1.

## 1. Bài toán đặt ra

Trong xác minh vân tay, ảnh probe có đường vân mờ hoặc đứt được so với một ảnh đăng ký gốc. Suy giảm có thể làm cặp cùng ngón bị từ chối hoặc không trích được đủ minutiae. Tuy nhiên, khôi phục ảnh gần ảnh tham chiếu theo sai số pixel không bảo đảm matcher phân biệt tốt hơn giữa cặp cùng ngón và khác ngón.

**Câu hỏi nghiên cứu:** So với cùng U-Net chỉ dùng L1, thêm triplet loss vào huấn luyện bộ phục hồi có giảm **FRR** (từ chối nhầm) ở mức hỏng nặng mô phỏng mà không làm tăng **FAR** (chấp nhận nhầm) tại bất kỳ DB nào, ở các ngưỡng khóa trước hay không? Kết quả có lặp lại trên các ngón giữ riêng và trên một bộ FVC khác không? Đây là **xác minh theo cặp**, không phải nhận dạng rank-1.

## 2. Công bố liên quan: phương pháp, kết quả và chỗ đứng của bài này

| Công trình | Phương pháp và kết quả báo cáo | Liên hệ với bài này |
|---|---|---|
| [Quality-adaptive enhancement, 2019](https://www.sciencedirect.com/science/article/pii/S0262885619300150) | Phân loại chất lượng rồi tăng cường thích ứng bằng Gabor/STFT/ODF; so bằng EER với NBIS và VeriFinger trên FVC2002/2004. | Tăng cường thích ứng và đánh giá bằng NBIS đã có tiền lệ. Gabor là đối chứng cổ điển; EER không phải FAR/FRR tại ngưỡng khóa của mình. |
| [Cheng et al., IEEE 2023](https://ieeexplore.ieee.org/document/10213986) | Huấn luyện nhiều giai đoạn để xử lý nhiễu và nối vân; CCRGAN tạo mẫu đăng ký giả lập. Trên FVC2002 DB1A, tác giả báo EER **0,05%** với MTS và **0,0009%** với biến thể dùng mẫu CCRGAN. | Gần về bài toán vân tay khô, nhưng khác cách tạo gallery, điều kiện ảnh và điểm vận hành. Không so số trực tiếp. |
| [Finger-UNet, 2023, preprint](https://arxiv.org/abs/2310.00629) | U-Net, L1 và nhánh phụ minutiae/hướng vân; dùng SFinGe. Bảng NBIS trên FVC2002 DB1 báo điểm cặp cùng ngón trung bình **52,77 → 74,01** từ raw sang mô hình. | Cùng họ kiến trúc và matcher; điểm genuine cao hơn chưa cho biết FAR thay đổi thế nào. |
| [FingerGAN, IEEE 2023](https://ieeexplore.ieee.org/document/10016755) | Phục hồi vân tay hiện trường (*latent*) bằng GAN với ràng buộc trên khung xương đường vân có trọng số theo minutiae và trên trường hướng. | Tiền lệ cho việc đưa tín hiệu cấu trúc vào **bộ phục hồi**, không phải ví dụ dùng triplet loss. |
| [Pan et al., DMD, 2025, preprint](https://arxiv.org/html/2507.15297v1) và [Beyond ROC-AUC, 2026, preprint](https://arxiv.org/html/2606.20680v1) | Công trình thứ nhất đề xuất biểu diễn dày cục bộ neo theo minutiae, báo rank-1/TAR tại FAR thấp/DET tùy bài toán; công trình thứ hai phân tích cách báo hiệu năng và khoảng bất định tại điểm vận hành. | DMD và đánh giá tại điểm vận hành là kỹ thuật kế thừa, không phải đóng góp mới của bài. |

### 2.1. Triplet loss trong các công trình vân tay

| Công trình | Triplet loss huấn luyện phần nào? | Kết quả và phạm vi đối chiếu |
|---|---|---|
| [Tang & Dai, IEEE BigDIA 2022](https://ieeexplore.ieee.org/document/9874011) | Huấn luyện CNN trích đặc trưng toàn ảnh ở bước đầu của hệ thống so khớp quy mô lớn; dùng cosine similarity để tìm ứng viên. | Tiền lệ dùng triplet cho **bộ trích đặc trưng so khớp**, không phải để cập nhật bộ phục hồi. Chưa xác minh số liệu từ toàn văn. |
| [Yang et al., IEEE ICMSS 2024](https://ieeexplore.ieee.org/document/10550678) | Kết hợp ResNeXt hai chiều với triplet loss cho nhận dạng vân tay. | Thêm tiền lệ dùng triplet cho **nhận dạng**. Tóm tắt không đủ để đối chiếu định lượng về dataset, ngưỡng hay kết quả. |
| [Ojha & Kumar, IEEE ICWITE 2024](https://doi.org/10.1109/ICWITE59797.2024.10503554) | Pix2Pix phục hồi ảnh; mạng Siamese học embedding bằng triplet loss, rồi chấm bằng khoảng cách Euclid. Bài không mô tả gradient triplet quay lại generator. | Tiền lệ gần nhất vì cùng có phục hồi và triplet. Hình 5 báo **80% trên 60 cặp SOCOFing**; Bảng II báo **86% trên FVC2000 DB1 Set B**. Không dùng các số này làm baseline trực tiếp cho FRR/FAR. |

**Khác ở vai trò của triplet loss, không phải ở ý tưởng dùng triplet.**

| Trục so sánh | Các công trình trên | Nghiên cứu này |
|---|---|---|
| **Thứ được học** | Tang & Dai dùng triplet cho bộ trích đặc trưng; Yang et al. kết hợp triplet với ResNeXt để nhận dạng. Ojha & Kumar có thêm bộ phục hồi Pix2Pix, nhưng phần phương pháp chỉ mô tả triplet huấn luyện Siamese, không mô tả truyền loss về Pix2Pix. | Bộ mô tả DMD giữ cố định. Gradient triplet đi qua điểm DMD và ảnh đầu ra để **cập nhật tham số U-Net**. Đầu ra của mô hình được huấn luyện là **ảnh phục hồi**, không phải embedding mới. |
| **Thứ được so trong loss** | Ojha & Kumar dùng khoảng cách Euclid giữa các embedding Siamese; Tang & Dai dùng cosine để tìm ứng viên ở bước so khớp. Không suy ra công thức loss của Yang et al. từ tóm tắt. | Ảnh probe sau phục hồi phải đạt điểm tương đồng DMD cao hơn mẫu khác ngón có điểm cao nhất trong **bảy ứng viên train** ít nhất một biên. Đây vẫn là mục tiêu xếp hạng kiểu triplet, chỉ khác điểm so sánh và đường gradient. |
| **Cách kiểm tra lợi ích** | Các bài trên dùng triplet trong hệ thống so khớp/nhận dạng của họ; kết quả không phải đối chứng L1 với L1 + triplet dưới giao thức NBIS của mình. | **NBIS không tham gia tính loss**. Cùng một U-Net có/không có loss phụ được đánh giá trên ảnh đầu ra, đo FRR/FAR theo DB ở ngưỡng khóa từ validation, trên tập giữ lại và FVC2004. |

**Câu chuyển sang phương pháp:** Thay vì dùng triplet để học một biểu diễn phục vụ so khớp, nghiên cứu này dùng điểm tương đồng từ một bộ mô tả cố định để hướng dẫn **phục hồi ảnh**, rồi kiểm tra xem lợi ích có chuyển sang một matcher khác hay không. Đây là điểm khác với các công trình đã rà soát, không phải tuyên bố lần đầu dùng triplet trực tiếp cho phục hồi.

Đây là rà soát có mục tiêu, không phải systematic review. Xem [ghi chú literature và đối chứng](./43_triplet_literature_gap_review.md) để tra thêm; trước khi nộp, rà lại bảng gốc và tình trạng xuất bản của các preprint.

## 3. Pain point và cách tiếp cận

**Pain point:** L1 chỉ thưởng tái tạo pixel. Điểm cùng ngón hoặc kết quả trung bình tốt hơn cũng có thể che việc một số cặp khác ngón được chấp nhận thêm. Cần đo cả FRR lẫn FAR, theo từng DB, ở điểm vận hành xác định trước.

**Cách tiếp cận:** So U-Net L1 với cùng U-Net bổ sung hàm mất mát `L1 + 0,1 × max(0, 0,2 + s_neg_max − s_pos)`. `s_pos` là điểm tương đồng DMD với mẫu cùng ngón; `s_neg_max` là điểm cao nhất trong các ứng viên khác ngón đã chọn từ tập train. Phần phụ phạt khi mẫu cùng ngón chưa cách mẫu khác ngón khó nhất đủ biên. Gradient đi qua điểm DMD về ảnh phục hồi rồi cập nhật U-Net; DMD giữ cố định. Khi đánh giá, **NBIS MINDTCT + BOZORTH3** chấm ảnh đầu ra, không phải mô hình dùng để tính loss.

**Vì sao có thể giúp:** Mục tiêu tương đồng bổ sung tín hiệu về khả năng phân biệt mà L1 không trực tiếp tối ưu. Đây là giả thuyết, không phải bảo đảm giảm FAR của NBIS: tín hiệu DMD chỉ là đại diện, và FAR thực đo còn phụ thuộc dữ liệu và ngưỡng.

## 4. Contribution chốt để viết

1. **Phương pháp và đối chứng:** Dùng điểm DMD cố định làm tín hiệu triplet để cập nhật **bộ phục hồi ảnh**, không huấn luyện một matcher mới. Đo tác động của việc thêm tín hiệu này bằng đối chứng L1 với L1 + triplet: cùng kiến trúc, khởi tạo, luồng mẫu và ngân sách trong mỗi seed; cùng quy tắc chọn checkpoint theo MAE validation, không nhất thiết chọn cùng epoch.
2. **Bằng chứng ở điểm vận hành khóa trước:** Báo cả dữ liệu giữ lại và dữ liệu ngoài, gồm FRR/FAR theo DB, số lượt đổi quyết định theo cặp và kết quả theo mức suy giảm. Trình bày cả trường hợp đạt và không đạt quy tắc đã khóa.
3. **Kết luận thực nghiệm:** Ở mức nặng mô phỏng, mức giảm FRR trung bình lặp lại, nhưng độ lớn và mức đánh đổi theo DB khác nhau. Không tuyên bố loss mới, SOTA, hay hiệu quả trên vân tay khô thật.

## 5. Thực nghiệm

### 5.1. Dataset và giao thức

- **FVC2000/2002 DB1–DB3:** Dùng cho train/validation và test giữ lại. Chia theo ID ngón có phạm vi trong DB và nhóm ảnh trùng byte; không khẳng định độc lập theo người xuyên DB/năm. Validation: 134 gallery, 938 probe, 21.518 cặp mỗi điều kiện. Test giữ lại: 145 gallery, 1.015 probe, 1.015 cặp cùng ngón và 24.388 cặp khác ngón mỗi điều kiện.
- **FVC2004 DB1–DB3:** Tập ngoài, giữ riêng khỏi huấn luyện và chọn ngưỡng. Gồm Set A và B: 330 gallery, 2.310 probe, 2.310 cặp cùng ngón và 251.790 cặp khác ngón mỗi điều kiện. Không dùng DB4 trong các phép thử chính.
- **Quy trình chung:** Impression 1 làm gallery không phục hồi; impressions 2–8 làm probe, ghép trong cùng DB. Chuẩn hóa 500 DPI, suy luận toàn ảnh FP32; cặp không so được tính là từ chối. Báo trung bình đều theo DB và độ nhạy loại ảnh trùng byte.
- **Ngưỡng:** [Test giữ lại](./41_triplet_heldout_test_protocol.md) dùng ngưỡng từng DB và từng mô hình lấy từ validation mức nặng theo trần FAR chung; không đồng nghĩa FAR bằng nhau. [Test FVC2004](./45_fvc2004_external_protocol.md) dùng trung vị sáu ngưỡng đã khóa: L1 **20**, triplet **22** cho cả ba DB. Không hiệu chỉnh trên test. Hai test dùng cùng checkpoint seed `20261127`: L1 epoch 1, triplet epoch 2.
- **SOCOFing:** Chỉ là pilot khả thi, không tính là test hiệu năng. Altered được tạo từ chính ảnh gốc dùng làm gallery, không phải hai lần lấy dấu độc lập.

### 5.2. Mô phỏng suy giảm: tiền lệ và phạm vi phù hợp

[Simulator](./06_structured_degradation_pilot.ipynb) tạo mặt nạ loang trơn trong vùng có kết cấu, dùng bộ lọc cực đại để làm mỏng vân tối rồi pha ảnh vùng đó về trắng. Ba mức nhẹ/vừa/nặng dùng tham số chọn vùng **0,15/0,30/0,45**, độ làm nhạt **0,40/0,65/0,85** và cửa sổ **3/3/5 px**. Tham số chọn vùng là phân vị để đặt mặt nạ mềm, không phải tỷ lệ pixel bị xóa chính xác. Seed xác định theo ảnh và điều kiện; cả hai nhánh nhận cùng probe. Ảnh gốc là tham chiếu trước can thiệp, không mặc định hoàn hảo.

**Cơ sở:** [SFinGe của Cappelli et al.](https://ieeexplore.ieee.org/document/1048096) là tiền lệ cho tạo ảnh vân tay tổng hợp; [tài liệu SFinGe](http://bias.csr.unibo.it/franco/SB/DispensePDF/SFinGe.pdf) mô tả erosion để mô phỏng da khô. Finger-UNet dùng SFinGe tạo cặp ảnh có suy giảm. **Bài này không chạy SFinGe** và không khẳng định mặt nạ, công thức pha hay ba mức của mình đã được công bố nguyên bản.

**Phù hợp làm stress test:** Mô phỏng trên ảnh thu từ cảm biến, có đầu vào ghép cặp và tái lập được. Pilot trên 12 probe train cho điểm NBIS giảm trung vị **7 / 26,5 / 57,5** theo ba mức. Điều đó kiểm tra độ khó, không hiệu chuẩn với độ ẩm da thật. Hai test dùng cùng họ suy giảm; FVC2004 kiểm tra chuyển bộ dữ liệu, không kiểm tra chuyển sang kiểu hỏng mới.

### 5.3. Thực nghiệm đã làm và kết quả

| Vai trò | Thực nghiệm | Kết quả cần đưa vào bài |
|---|---|---|
| Kiểm tra mô phỏng | Pilot simulator trên train | Điểm NBIS giảm theo mức; không dùng như bằng chứng hiệu năng. |
| Đối chứng validation | [Gabor](./16_gabor_validation_matching.ipynb), [seed gốc](./38_native_counterfactual_nbis_validation.ipynb), [seed lặp](./40_native_triplet_replication_validation.ipynb) | Trung bình ba mức mô phỏng, FRR/FAR (%): raw **32,142/0,368**; Gabor **38,905/0,564**; L1 **19,758/0,584** và **20,491/0,601**; triplet **18,121/0,603** và **18,571/0,629**. Cùng ngưỡng gốc theo DB. Thử nghiệm seed gốc còn có warmstart và hai loss rủi ro; để phụ lục nếu cần. |
| Phân tích validation dưới trần FAR | Hai seed, mức nặng, đặt trần theo số nhận nhầm của L1 tại ngưỡng gốc | FRR **36,34% → 33,10%** và **38,65% → 35,81%**. Đây là kết quả validation dưới trần chung, không phải hai lần xác nhận trên test hay so tại FAR thực đo bằng nhau. |
| Test giữ lại | [FVC2000/2002](./41_triplet_heldout_results.md) | Mức nặng: FRR **37,76% → 33,57%**, FAR **0,184% → 0,076%**; **FAIL** vì FVC2000/DB2 tăng **3 → 4** nhận nhầm trên 1.904 cặp khác ngón. |
| Test ngoài | [FVC2004](./45_fvc2004_external_nbis_test.ipynb) | Mức nặng: FRR **38,61% → 38,05%**, FAR **0,498% → 0,283%**; **PASS**, không DB nào tăng FAR. Lỗi giảm ròng **13 từ chối nhầm và 541 chấp nhận nhầm**. DB2 đóng góp phần lớn mức giảm từ chối nhầm, DB3 giảm nhiều nhận nhầm nhất nhưng có thêm một từ chối nhầm. |
| Kiểm tra khả thi | [SOCOFing](./44_socofing_nbis_feasibility_pilot.ipynb), 12 người | **19/120** gallery đạt tối thiểu 10 minutiae; có điểm cho **41/56/55 trên 993** cặp cùng ngón ở raw/L1/triplet. Không kết luận hiệu năng so khớp khi độ phủ thấp; đưa vào giới hạn hoặc phụ lục. |

**Tiêu chí đạt của hai test:** FRR trung bình ở mức nặng phải giảm và FAR không tăng ở bất kỳ DB nào. Cả hai test đều cho thấy với ảnh gốc và hai mức nhẹ hơn, triplet giảm FAR trung bình nhưng tăng FRR trung bình. Bản thảo chính cần bảng đủ bốn điều kiện và số theo DB ở mức nặng; không chỉ đưa hàng tốt nhất. Raw/Gabor là đối chứng validation, không ghép vào bảng test như thể đã được chạy trên test.

## 6. Nhận xét, giới hạn và kết luận

- **Điểm mạnh:** Đối chứng sát câu hỏi, kiểm tra lặp seed trên validation, hai tập test có giao thức khóa, chấm bằng NBIS và công bố đánh đổi thay vì chỉ chọn chỉ số có lợi.
- **Điểm yếu:** Không có đo độ khô thực tế; cùng simulator trên train và test; chỉ một matcher đánh giá chính; test chỉ dùng một seed huấn luyện. Ngưỡng L1 và triplet khác nhau, nên kết quả chính là so sánh **hai pipeline tại điểm vận hành đã khóa**, không tách được mức ảnh hưởng riêng của ngưỡng trên test. Các cặp dùng chung probe/gallery; PASS/FAIL không phải kiểm định thống kê. Kết quả SOCOFing phản ánh độ phủ NBIS hiện tại, không chứng minh dataset thiếu đặc trưng.
- **Đánh đổi có đáng không?** So với raw ở seed gốc trên validation, cả pipeline triplet giảm FRR **14,02 điểm phần trăm** trung bình ba mức (**29,28** ở mức nặng), đổi lấy FAR tăng **0,235 điểm** (**0,290** ở mức nặng). Với 10.000 lượt mỗi loại, trung bình tương đương khoảng **1.402 lượt từ chối nhầm tránh được** và **24 lượt nhận nhầm thêm**. Đây là minh họa, không phải lưu lượng triển khai. Nếu có trần FAR thì phải thỏa trần trước; nếu không, cân chi phí lỗi theo lưu lượng thật. Không gán lợi ích raw → triplet hoàn toàn cho loss triplet.
- **Kết luận để viết:** Tín hiệu triplet trực tiếp lên bộ phục hồi có ích ở mức nặng mô phỏng, nhưng hiệu quả phụ thuộc DB, mức suy giảm và ngưỡng. Không đủ cơ sở thay L1 làm mặc định chung.

**Thứ tự hoàn thiện bản thảo:** Viết Introduction từ mục 1/3/4; Related Work từ mục 2; Methods và Experimental Setup từ mục 3/5.1/5.2; Results tách validation khỏi hai test; Discussion đặt PASS và FAIL cạnh nhau. Trước khi chốt Abstract, nên bổ sung khoảng bất định cho hiệu ứng mức nặng bằng điểm đã lưu, dùng phân tích có tính đến phụ thuộc do dùng chung ngón/probe/gallery. Đây là việc **chưa làm**; không cần đổi ngưỡng hay chạy lại test.
