# Kịch Bản Thuyết Minh 18 Slide Đồ Án Môn Học Máy Học (15 Phút)

> **Đề tài:** Ứng dụng các thuật toán học máy trong phân loại ảnh cháy rừng (DeepFire Dataset)  
> **Thời lượng:** 12–15 phút (~40–45 giây mỗi slide; dành thời gian phân tích biểu đồ và trả lời câu hỏi của Thầy)

---

## Slide 1 — Trang bìa & Tổng quan kết quả thực nghiệm
* **Thời gian:** 40 giây
* **Lời thoại:**
  > "Kính thưa quý Thầy Cô trong Hội đồng chấm đồ án môn học Máy học. Hôm nay, em xin đại diện nhóm trình bày đồ án: **'Ứng dụng các thuật toán học máy trong phân loại ảnh cháy rừng'** trên bộ dữ liệu DeepFire gồm 1.900 ảnh.
  > Đồ án tuân thủ nghiêm ngặt phương pháp luận khoa học: kiểm toán dữ liệu bằng hàm băm dHash để chống rò rỉ thông tin giữa Train và Test; trích xuất đặc trưng kết hợp màu sắc HSV và cấu trúc HOG; nén chiều bằng PCA; và so sánh công bằng 4 thuật toán kinh điển.
  > Kết quả nổi bật: Mô hình **SVM (RBF)** được lựa chọn khách quan từ tập Validation đã đạt **F1-Score 94,03%**, **Recall 95,26%** và **Accuracy 93,95%** trên 380 ảnh kiểm thử độc lập, chỉ bỏ sót 9 vụ cháy. Toàn bộ mã nguồn, dữ liệu và mô hình đều có thể tái lập 100%."

---

## Slide 2 — Mục tiêu đồ án & Bài toán phân loại
* **Thời gian:** 45 giây
* **Lời thoại:**
  > "Đồ án bám sát 5 mục tiêu cốt lõi theo đề cương của Thầy: (1) Phân tích chuyên sâu dữ liệu ảnh; (2) Tiền xử lý chuẩn mực chống data leakage; (3) Cài đặt ít nhất 3 mô hình học máy; (4) Đánh giá và chọn ra mô hình tối ưu; (5) Phân tích kết quả, ma trận nhầm lẫn và lỗi thực tế.
  > Về bài toán: Đầu vào là một ảnh RGB phong cảnh rừng, đầu ra là nhãn nhị phân 0 (Không cháy) hoặc 1 (Cháy). Đây là bài toán phân loại toàn ảnh (whole-image classification) nhằm hỗ trợ tự động sàng lọc ảnh từ trạm quan trắc hoặc drone.
  > Nhóm xin nêu rõ ranh giới khoa học: Đồ án tập trung vào phân loại, chưa thực hiện khoanh vùng bounding box hay dự báo cháy trong tương lai."

---

## Slide 3 — Mô tả bộ dữ liệu DeepFire & Kiểm toán chống rò rỉ
* **Thời gian:** 50 giây
* **Lời thoại:**
  > "Bộ dữ liệu DeepFire do A. Khan và cộng sự công bố gồm 1.900 ảnh, được gán nhãn theo tên file nofire_ (lớp 0) và fire_ (lớp 1). Tỷ lệ giữa hai lớp là 1:1 (950 ảnh mỗi lớp), do đó dữ liệu hoàn toàn cân bằng, không gặp hiện tượng mất cân bằng lớp.
  > Điểm đặc biệt của đồ án là quy trình **Kiểm toán dữ liệu (Data Auditing)**:
  > - Dùng SHA-256 loại bỏ 2 ảnh trùng pixel hoàn toàn.
  > - Dùng mã băm dHash 64-bit với khoảng cách Hamming nhỏ hơn hoặc bằng 4 để phát hiện các cụm ảnh gần trùng (near-duplicates).
  > - Nhóm đã loại 2 ảnh Train dính nhóm với Test và dùng `StratifiedGroupKFold` để chia tập: 1.213 ảnh Train, 303 ảnh Validation và 380 ảnh Test. Các cụm dHash tuyệt đối không giao nhau giữa các tập, triệt tiêu nguy cơ rò rỉ dữ liệu."

---

## Slide 4 — EDA 1: Phân bố lớp & Tính đa dạng hình thái
* **Thời gian:** 45 giây
* **Lời thoại:**
  > "Quan sát biểu đồ phân bố bên trái, tỷ lệ hai lớp trên cả 3 tập Train, Val và Test đều duy trì mức cân bằng lý tưởng 50:50.
  > Nhìn vào 8 ảnh mẫu bên phải: Ảnh cháy có hình thái rất đa dạng: có ngọn lửa bùng phát cao trong đêm tối, có đám cháy âm ỉ dưới mặt đất, và có trường hợp khói trắng dày đặc che phủ toàn bộ khung hình. Ở chiều ngược lại, lớp không cháy gồm nhiều địa hình núi đá, cây cối rậm rạp và đặc biệt là tán lá mùa thu ngả màu vàng đỏ.
  > Kết luận EDA quan trọng: Chúng ta không thể chỉ dựa vào một ngưỡng màu đỏ duy nhất để nhận diện cháy rừng, mà bắt buộc phải kết hợp cả màu sắc lẫn kết cấu đường viền."

---

## Slide 5 — EDA 2: Kích thước, Chất lượng ảnh & Phân bố màu sắc
* **Thời gian:** 45 giây
* **Lời thoại:**
  > "Tiếp tục phân tích kỹ thuật:
  > - Về kích thước: Dù công bố là 250x250 nhưng thực tế có 73 ảnh kích thước 256x256 và 1 ảnh 252x252. Vì vậy, bước resize chuẩn hóa là bắt buộc.
  > - Về độ sáng: Lớp cháy có độ sáng trung bình 0.339, tối hơn lớp không cháy 0.401 do khói che khuất hoặc chụp ban đêm.
  > - Về phân bố Hue: Kênh màu Hue của lớp cháy lệch hẳn về dải màu ấm (đỏ, cam, vàng) với cường độ Red trung bình 0.476, vượt trội so với 0.377 của lớp không cháy.
  > - Ảnh trung bình (Mean Images) thể hiện rõ xu hướng tập trung sắc cam ở trung tâm của lớp cháy, nhưng do vị trí ngọn lửa ngẫu nhiên nên không thể dùng mặt nạ vị trí cố định."

---

## Slide 6 — Tiền xử lý dữ liệu & Trích xuất đặc trưng
* **Thời gian:** 50 giây
* **Lời thoại:**
  > "Quy trình tiền xử lý và trích xuất đặc trưng gồm 4 bước khép kín:
  > 1. Chuẩn hóa ảnh: Đưa về RGB, resize thống nhất 96x96 pixel và chuẩn hóa giá trị pixel về đoạn [0, 1].
  > 2. Trích xuất màu sắc: Dùng Color Histogram không gian màu HSV với 32 bins Hue, 16 bins Saturation và 16 bins Value, tạo ra vector 64 chiều.
  > 3. Trích xuất kết cấu viền: Dùng bộ mô tả HOG với 8 hướng gradient, cell 16x16, block 2x2, thu được 800 chiều đặc trưng đường nét.
  > 4. Ghép vector đạt 864 chiều, sau đó đưa qua `StandardScaler` và `PCA` giữ 95% phương sai, nén xuống còn 231 thành phần chính.
  > Cực kỳ quan trọng: StandardScaler và PCA được đóng gói trong `Pipeline`, chỉ fit trên fold Train của từng lần kiểm tra chéo, tuyệt đối không fit trên dữ liệu Test."

---

## Slide 7 — Bốn mô hình Machine Learning & Không gian tìm kiếm tham số
* **Thời gian:** 40 giây
* **Lời thoại:**
  > "Để so sánh toàn diện, nhóm cài đặt 4 mô hình đại diện cho các trường phái học máy khác nhau:
  > 1. **Logistic Regression:** Mô hình phân loại tuyến tính đối chứng, tìm kiếm hệ số điều hòa C trong {0.1, 1, 10}.
  > 2. **K-Nearest Neighbors (KNN):** Mô hình phân loại theo khoảng cách không gian đặc trưng, tìm k trong {3, 5, 9} và trọng số uniform hoặc distance.
  > 3. **Support Vector Machine (SVM):** Tìm siêu phẳng biên cực đại với kernel RBF phi tuyến, tìm C trong {1, 10}.
  > 4. **Random Forest:** Ensemble học tập đa cây, n_estimators=150, max_depth trong {12, None}.
  > Quá trình tìm kiếm siêu tham số thực hiện bằng `GridSearchCV` với 3-fold StratifiedGroupKFold trên 1.213 ảnh Train."

---

## Slide 8 — Kết quả Cross-Validation & Khóa mô hình trên Validation
* **Thời gian:** 45 giây
* **Lời thoại:**
  > "Bảng trên thể hiện kết quả kiểm tra chéo 3 folds: SVM đạt F1 trung bình 93,66% với độ lệch chuẩn cực kỳ ổn định (+/- 0,46%), trong khi Logistic Regression đạt 93,79%.
  > Khi đánh giá trên tập Validation độc lập 303 ảnh:
  > - **SVM vươn lên dẫn đầu với F1 94,19%** và Recall 95,39%, vượt qua Logistic Regression (93,42%).
  > - Random Forest chỉ đạt F1 86,45% do PCA làm suy giảm tính trực giao của các cây quyết định.
  > - KNN đạt thấp nhất ở mức 71,54%.
  > Tuân thủ tính liêm chính học thuật: Quyết định chọn **SVM** được ghi nhận vào file `selection_before_test.json` TRƯỚC KHI đánh giá trên tập Test. Nhóm tuyệt đối không dùng Test để cherry-pick tham số."

---

## Slide 9 — Đánh giá hiệu năng 4 mô hình trên tập Test (380 ảnh)
* **Thời gian:** 50 giây
* **Lời thoại:**
  > "Đây là bảng kết quả kiểm thử thực tế trên 380 ảnh Test độc lập (190 Cháy, 190 Không cháy):
  > - **SVM xuất sắc dẫn đầu toàn diện**: Đạt Accuracy 93,95% (đúng 357/380 ảnh), Precision 92,82%, Recall 95,26% và F1-Score 94,03%.
  > - **Logistic Regression là đối chứng rất mạnh**: Đạt F1 92,67%, chỉ kém SVM 1,36 điểm phần trăm (tương đương lệch đúng 5 bức ảnh).
  > - **Random Forest**: Đạt F1 87,47% và Accuracy 87,63%.
  > - **KNN tụt hậu nghiêm trọng**: Recall chỉ đạt 53,16% và F1 67,56%. Mặc dù Precision cao (92,66%), nhưng KNN bỏ sót tới gần một nửa số vụ cháy, cho thấy việc tính khoảng cách Euclidean trong không gian 231 chiều bị nhiễu nghiêm trọng."

---

## Slide 10 — Báo cáo phân loại chi tiết (Classification Report đầy đủ)
* **Thời gian:** 45 giây
* **Lời thoại:**
  > "Để đáp ứng yêu cầu chi tiết của Thầy, nhóm trình bày bảng Classification Report đầy đủ cho cả 2 lớp của cả 4 mô hình:
  > - Với SVM: Mô hình đạt sự cân bằng tuyệt hảo giữa 2 lớp: F1 lớp Không cháy đạt 93,87% và F1 lớp Cháy đạt 94,03%. Macro Average và Weighted Average đều đạt 93,95%.
  > - Logistic Regression cũng duy trì sự ổn định cao với F1 cả hai lớp đều xấp xỉ 92,6%.
  > - Ngược lại, KNN bị mất cân bằng trầm trọng: F1 lớp 0 là 78,96% nhưng F1 lớp 1 chỉ có 67,56%. KNN có xu hướng thiên vị đoán về lớp Không cháy để an toàn (Recall lớp 0 lên đến 95,79%), dẫn đến thảm họa bỏ sót cháy rừng ngoài thực tế."

---

## Slide 11 — Phân tích ma trận nhầm lẫn (Confusion Matrix)
* **Thời gian:** 50 giây
* **Lời thoại:**
  > "Ma trận nhầm lẫn bên trái trả lời trực tiếp câu hỏi: **'Model hay nhầm class nào?'**:
  > - Mô hình SVM: Trong 190 ảnh không cháy, SVM chỉ báo nhầm 14 ảnh (FP = 7,37%). Trong 190 ảnh cháy thật, SVM chỉ bỏ sót đúng 9 ảnh (FN = 4,74%). Trong bài toán phòng cháy chữa cháy, chi phí bỏ sót đám cháy (FN) nguy hiểm hơn báo nhầm (FP), và SVM đã làm rất tốt việc kiềm chế FN ở mức tối thiểu.
  > - Logistic Regression bỏ sót 13 ảnh và báo nhầm 16 ảnh.
  > - Random Forest bỏ sót 26 ảnh và báo nhầm 21 ảnh.
  > - Đáng báo động nhất là KNN: Bỏ sót tới **89 trên 190 ảnh cháy** (chiếm 46,84%). KNN hoàn toàn không phù hợp cho bài toán cảnh báo cháy."

---

## Slide 12 — So sánh Train vs Validation: Đánh giá học quá khớp (Overfitting)
* **Thời gian:** 45 giây
* **Lời thoại:**
  > "So sánh giữa điểm Train và Validation để trả lời câu hỏi về Overfitting:
  > - Cả SVM, Logistic Regression và Random Forest đều đạt F1 Train tuyệt đối 100%. Điều này dễ hiểu vì không gian 231 chiều đặc trưng đủ lớn để phân tách trọn vẹn 1.213 ảnh huấn luyện.
  > - Tuy nhiên, khoảng cách giữa Train và Validation bộc lộ rõ năng lực khái quát hóa:
  >   + **SVM kiểm soát overfitting tốt nhất**: Khoảng chênh lệch chỉ 5,81 điểm phần trăm (Train 100% vs Val 94,19%).
  >   + Logistic Regression chênh 6,58%.
  >   + **Random Forest overfit nặng nhất**: Chênh tới 13,55% (Val chỉ đạt 86,45%).
  > Nguyên nhân SVM kiểm soát overfitting tốt là nhờ nguyên lý Biên Cực Đại (Maximum Margin), đóng vai trò như một cơ chế regularization tự nhiên."

---

## Slide 13 — Phân tích đường học (Learning Curve của SVM)
* **Thời gian:** 45 giây
* **Lời thoại:**
  > "Nhìn vào biểu đồ Learning Curve của SVM theo số lượng mẫu huấn luyện trong từng fold:
  > - Khi kích thước tập học tăng từ 283 mẫu (35%) lên 525 mẫu (65%) rồi 809 mẫu (100%), điểm F1 Cross-Validation tăng trưởng đều đặn từ 91,00% lên 92,62% rồi đạt đỉnh 93,66%.
  > - Điểm Train vẫn duy trì 100% trong khi đường Validation tiếp tục có xu hướng đi lên.
  > Ý nghĩa khoa học: Mô hình không bị ghi nhớ máy móc hay bão hòa dữ liệu. Việc bổ sung thêm các bộ ảnh phong cảnh rừng mới trong tương lai chắc chắn sẽ tiếp tục nâng cao độ chính xác của SVM."

---

## Slide 14 — Phân tích lỗi thực tế: Ảnh mờ hay rõ? Nguyên nhân nhầm lẫn
* **Thời gian:** 50 giây
* **Lời thoại:**
  > "Đây là phần trả lời sâu sắc cho câu hỏi: **'Ảnh mờ hay rõ ảnh hưởng thế nào?'**:
  > Nhóm đã tính toán định lượng thuộc tính của các ảnh dự đoán sai trên tập Test:
  > - Nhóm dự đoán Đúng: Độ sáng trung bình 0.371, độ sắc nét Laplacian đạt 1.686,2.
  > - **Nhóm Bỏ sót (False Negative - 9 ảnh)**: Độ sáng thấp hơn (0.322) và **độ sắc nét Laplacian chỉ đạt 559,2 — mờ hơn gấp 3 lần so với ảnh đúng!**
  > Bằng chứng số liệu khẳng định: Ảnh mờ, mất nét hoặc bị khói dày che khuất chính là thủ phạm làm triệt tiêu các đặc trưng cạnh của HOG, khiến mô hình bỏ sót.
  > Về 14 ảnh Báo nhầm (FP): Chủ yếu rơi vào ảnh sương mù trắng dày trên ngọn cây (nofire_0400) hoặc cây cối ngả màu vàng đỏ mùa thu (nofire_0422), làm đánh lừa histogram màu HSV."

---

## Slide 15 — Trả lời toàn diện 8 câu hỏi đề cương của Thầy
* **Thời gian:** 50 giây
* **Lời thoại:**
  > "Slide 15 tổng hợp cô đọng câu trả lời cho toàn bộ 8 câu hỏi bắt buộc trong mục 3.5 của Thầy:
  > 1. *Model nào tốt nhất?* -> SVM (RBF, C=10) dẫn đầu với F1 Test 94,03%.
  > 2. *Chênh lệch bao nhiêu?* -> SVM hơn LR 1,36%, hơn RF 6,56% và hơn KNN 26,47%.
  > 3. *Phân tích metrics?* -> SVM ưu tiên Recall cao (95,26%) để hạn chế lọt đám cháy, Precision đạt 92,82%.
  > 4. *Hay nhầm class nào?* -> KNN nhầm nặng lớp Cháy thành Không cháy; SVM nhầm rất ít (14 FP, 9 FN).
  > 5. *Ảnh mờ/rõ thế nào?* -> Ảnh mờ (Laplacian 559) là nguyên nhân chính gây bỏ sót cháy.
  > 6. *Train vs Val có overfit không?* -> Overfit nhẹ ở SVM (5,81%), overfit nặng ở Random Forest (13,55%).
  > 7. *Model nào phù hợp?* -> SVM RBF phù hợp nhất nhờ phân tách ranh giới phi tuyến tốt.
  > 8. *Yếu tố ảnh hưởng?* -> Kích thước resize 96x96, phép nén PCA, thời tiết sương mù và lá mùa thu."

---

## Slide 16 — Kết luận & Bảng đối chiếu yêu cầu đề tài đồ án
* **Thời gian:** 40 giây
* **Lời thoại:**
  > "Bảng đối chiếu khẳng định đồ án đã hoàn thành đầy đủ 100% cả 10 mục nội dung theo đề cương của Thầy: từ kiểm toán dataset, EDA, tiền xử lý, mô hình hóa đến phân tích chi tiết.
  > Thành quả lớn nhất của nhóm là xây dựng được một pipeline thị giác máy tính truyền thống hoàn chỉnh, khách quan, không rò rỉ dữ liệu và đạt độ chính xác thực tế 93,95% trên tập kiểm thử độc lập."

---

## Slide 17 — Hướng phát triển & Triển khai thực tế
* **Thời gian:** 40 giây
* **Lời thoại:**
  > "Để đưa nghiên cứu từ phòng thí nghiệm ra ứng dụng thực địa, nhóm đề xuất 4 hướng phát triển:
  > 1. Huấn luyện trên dữ liệu mất cân bằng thực tế (nơi ảnh rừng bình thường chiếm >99%), tinh chỉnh ngưỡng quyết định Threshold Moving.
  > 2. Tích hợp phân tích chuỗi video qua thời gian (Temporal Smoothing) để lọc nhiễu nhấp nháy do gió và sương.
  > 3. Nâng cấp sang Deep Learning (YOLOv8/v11) để khoanh vùng tọa độ ngọn lửa bằng Bounding Box.
  > 4. Tối ưu hóa mô hình nhúng (Edge AI qua ONNX) để lắp trực tiếp trên thiết bị camera của drone tuần tra."

---

## Slide 18 — Sản phẩm bàn giao, Demo suy luận & Lời cảm ơn
* **Thời gian:** 45 giây
* **Lời thoại:**
  > "Toàn bộ sản phẩm bàn giao gồm có: File báo cáo Word 10 mục chuẩn; Slide PPTX 18 trang; File Jupyter Notebook chạy 1 click trên Google Colab; và trọn bộ mã nguồn cùng 4 mô hình đã train sẵn.
  > Để demo suy luận nhanh một ảnh bất kỳ, chỉ cần chạy lệnh: `python src/predict.py duong_dan_anh.jpg`.
  > Chúng em xin chân thành cảm ơn Quý Thầy Cô trong Hội đồng đã lắng nghe và rất mong nhận được những nhận xét, góp ý quý báu. Kính chúc Quý Thầy Cô sức khỏe và thành công!"
