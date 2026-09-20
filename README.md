# MayHoc - Phân Loại Ảnh Cháy Rừng (Forest Fire Image Classification)

> **Đồ án môn học Máy học (Machine Learning)**  
> **Tác giả:** Cáp Phạm Đình Thăng  
> **Bộ dữ liệu:** DeepFire / Forest Fire Dataset (CC BY 4.0)

---

## Giới thiệu đề tài

Dự án nghiên cứu và triển khai ứng dụng các thuật toán **Học máy cổ điển (Classical Machine Learning)** để giải quyết bài toán **phân loại ảnh nhị phân: Cháy (Fire) và Không cháy (No Fire)**. 

Hệ thống được thiết kế theo quy chuẩn nghiên cứu thực nghiệm nghiêm ngặt:
- **Chống rò rỉ dữ liệu (Data Leakage)**: Sử dụng thuật toán dHash (Difference Hash) để phát hiện và cô lập các nhóm ảnh gần trùng lặp, đảm bảo không có ảnh tương tự nhau cùng xuất hiện ở cả hai tập Train và Test.
- **Trích xuất đặc trưng thị giác kết hợp**: Kết hợp giữa thông tin màu sắc (HSV Color Histogram) và đặc trưng cạnh/cấu trúc không gian (Histogram of Oriented Gradients - HOG) với tổng cộng 864 chiều.
- **Tối ưu hóa & Giảm chiều**: Sử dụng `StandardScaler` và `PCA` (giữ 95% phương sai giải thích) nằm gói gọn trong từng pipeline Cross-Validation.
- **Đánh giá khách quan**: Khóa lựa chọn mô hình dựa trên chỉ số F1 lớp Cháy trên tập Validation trước khi thực hiện đánh giá độc lập trên tập Test chưa từng nhìn thấy.
- **Ứng dụng Web tương tác**: Cung cấp giao diện Web Fullstack (FastAPI + React Vite) và Web App gọn nhẹ hỗ trợ tải ảnh, dự đoán thời gian thực, xem xác suất phân loại và so sánh kết quả giữa các mô hình.

---

## Cấu trúc thư mục dự án

```text
MayHoc/
├── backend/                  # FastAPI REST API phục vụ suy luận mô hình
│   └── main.py
├── frontend/                 # Giao diện Web tương tác (React 19 + Vite + Tailwind/Lucide)
│   ├── src/
│   ├── index.html
│   ├── package.json
│   └── vite.config.js
├── web/                      # Ứng dụng Web FastAPI gọn nhẹ tích hợp UI tĩnh
│   ├── app.py
│   └── static/
├── models/                   # Các mô hình học máy đã huấn luyện (.joblib)
│   ├── Logistic_Regression.joblib
│   ├── KNN.joblib
│   ├── SVM.joblib
│   ├── Random_Forest.joblib
│   ├── scaler.joblib
│   └── pca.joblib
├── notebooks/                # Jupyter / Google Colab Notebook hoàn chỉnh
│   └── MayHoc_Chay_rung.ipynb
├── reports/                  # Báo cáo học phần
│   ├── Bao_cao_MayHoc_Chay_rung.docx  # Báo cáo Word chuẩn 10 mục
│   ├── Bao_cao_MayHoc_Chay_rung.md    # Báo cáo định dạng Markdown
│   └── figures/                       # Biểu đồ EDA, Confusion Matrix, Learning Curve
├── slides/                   # Slide thuyết trình đồ án
│   └── Bao_cao_MayHoc_Chay_rung.pptx
├── results/                  # Dữ liệu thực nghiệm, ma trận nhầm lẫn, file JSON/CSV
│   ├── model_metrics.csv
│   ├── confusion_matrices.json
│   ├── classification_reports.json
│   ├── dataset_audit.json
│   ├── predictions.csv
│   └── summary.json
├── src/                      # Mã nguồn quy trình thực nghiệm
│   ├── experiment.py         # Toàn bộ pipeline: Tải dữ liệu, EDA, CV, Huấn luyện, Đánh giá
│   └── predict.py            # CLI dự đoán nhãn cho 1 ảnh đơn lẻ
├── data/                     # Thư mục chứa dữ liệu ảnh (bị bỏ qua bởi Git)
│   └── raw/
├── requirements.txt          # Danh sách thư viện Python cần thiết
├── run_all.bat               # Script khởi động đồng thời Backend (port 8000) & Frontend (port 3000)
├── run_web.bat               # Script khởi động Web Server gọn nhẹ (port 8000)
├── run_backend.bat           # Script khởi động Backend FastAPI riêng biệt
├── run_frontend.bat          # Script khởi động Frontend Vite riêng biệt
└── README.md                 # Tài liệu hướng dẫn đồ án
```

---

## Pipeline trích xuất đặc trưng & Tiền xử lý

1. **Chuẩn hóa kích thước ảnh**: Ảnh đầu vào được đưa về kích thước cố định $96 \times 96$ pixels (đảm bảo cân bằng giữa thời gian tính toán và độ chi tiết).
2. **Trích xuất đặc trưng màu sắc (HSV Color Histogram - 64 chiều)**:
   - Kênh Hue (H): 32 bins (nhận diện sắc tố vàng, cam, đỏ đặc trưng của lửa).
   - Kênh Saturation (S): 16 bins (đo lường độ bão hòa màu).
   - Kênh Value (V): 16 bins (đo lường độ sáng).
3. **Trích xuất đặc trưng cấu trúc (HOG - 800 chiều)**:
   - Số hướng gradient: 8 orientations.
   - Kích thước cell: $16 \times 16$ pixels/cell.
   - Khối chuẩn hóa: $2 \times 2$ cells/block.
4. **Chuẩn hóa & Giảm chiều**:
   - Vector kết hợp $864$ chiều $\rightarrow$ `StandardScaler` (chuẩn hóa $z$-score).
   - `PCA (variance=0.95)`: Giảm xuống còn **231 thành phần chính**, bảo toàn 95% lượng thông tin phương sai và loại bỏ nhiễu dư thừa.

---

## Bảng so sánh kết quả thực nghiệm

Kết quả kiểm thử trên tập dữ liệu độc lập (**Test Set: 380 ảnh - 190 Cháy, 190 Không cháy**):

| Thuật toán | CV F1-Score | Validation F1 | Test Accuracy | Test Precision | Test Recall | Test F1-Score | Tốc độ suy luận |
|:---|:---:|:---:|:---:|:---:|:---:|:---:|:---:|
| **Support Vector Machine (SVM)** ⭐ | **93.66%** | **94.19%** | **93.95%** | **92.82%** | **95.26%** | **94.03%** | 0.68 ms/ảnh |
| **Logistic Regression** | 93.79% | 93.42% | 92.63% | 92.19% | 93.16% | 92.67% | 0.02 ms/ảnh |
| **Random Forest** | 88.36% | 86.45% | 87.63% | 88.65% | 86.32% | 87.47% | 0.29 ms/ảnh |
| **K-Nearest Neighbors (KNN)** | 75.05% | 71.54% | 74.47% | 92.66% | 53.16% | 67.56% | 0.08 ms/ảnh |

> ⭐ **Mô hình tối ưu được lựa chọn:** **Support Vector Machine (SVM)** (với kernel RBF, $C=10$, $\gamma='scale'$).  
> SVM đạt điểm cân bằng vượt trội giữa độ chính xác tổng quát (Accuracy 93.95%) và khả năng bắt trúng các đám cháy thực tế (Recall 95.26%), chỉ bỏ sót 9 trên tổng số 190 trường hợp ảnh cháy trong tập kiểm thử.

---

## Hướng dẫn cài đặt & Chạy dự án

### 1. Yêu cầu hệ thống
- Python 3.10, 3.11 hoặc 3.12 (khuyến nghị 3.12)
- Node.js >= 18.x (nếu muốn khởi chạy Frontend React)
- Git

### 2. Cài đặt môi trường Python
Mở Terminal / PowerShell tại thư mục gốc `MayHoc`:

```bash
# Tạo môi trường ảo (tùy chọn nhưng khuyến khích)
python -m venv venv
venv\Scripts\activate      # Trên Windows
# source venv/bin/activate  # Trên Linux / macOS

# Cài đặt các thư viện phụ thuộc
python -m pip install -r requirements.txt
```

---

### 3. Huấn luyện lại toàn bộ mô hình (Re-train Pipeline)

Nếu muốn tự động tải lại dữ liệu từ nguồn mở Kaggle và chạy lại toàn bộ quy trình EDA, tìm siêu tham số (GridSearchCV), huấn luyện và xuất báo cáo:

```bash
python src/experiment.py --download
```
*Dung lượng bộ dữ liệu khoảng 149 MB. Quá trình xử lý và huấn luyện mất khoảng 1-2 phút.*

---

### 4. Dự đoán ảnh bằng dòng lệnh (CLI)

Dự đoán nhanh một bức ảnh bất kỳ bằng mô hình tốt nhất (SVM):

```bash
python src/predict.py path/to/image.jpg
```

Kết quả trả về định dạng JSON:
```json
{"model": "SVM", "label": 1, "class": "Cháy"}
```

---

### 5. Khởi chạy ứng dụng Web trực quan

#### Cách 1: Chạy toàn bộ hệ thống Fullstack (FastAPI + React Vite)
- **Trên Windows**: Nhấp đúp vào file `run_all.bat`.
- **Hoặc chạy thủ công qua 2 cửa sổ dòng lệnh:**
  - *Cửa sổ 1 (Backend)*:
    ```bash
    python -m uvicorn backend.main:app --host 127.0.0.1 --port 8000 --reload
    ```
  - *Cửa sổ 2 (Frontend)*:
    ```bash
    cd frontend
    npm install
    npm run dev
    ```
  - Truy cập trình duyệt tại: **http://localhost:3000** (API Docs tại: **http://127.0.0.1:8000/docs**).

#### Cách 2: Chạy Web App tĩnh gọn nhẹ
- **Trên Windows**: Nhấp đúp vào file `run_web.bat`.
- **Hoặc dòng lệnh**:
  ```bash
  python -m uvicorn web.app:app --host 0.0.0.0 --port 8000 --reload
  ```
- Truy cập trình duyệt tại: **http://localhost:8000**.

---

### 6. Chạy trên Google Colab / Jupyter Notebook
1. Truy cập [Google Colab](https://colab.research.google.com/).
2. Chọn **Upload notebook** và tải file `notebooks/MayHoc_Chay_rung.ipynb`.
3. Chọn **Runtime -> Run all**. Toàn bộ mã nguồn, tải dữ liệu, trích xuất đặc trưng và biểu đồ đều được cấu hình độc lập tự động.

---

## Bộ dữ liệu & Giấy phép sử dụng

- **Bộ dữ liệu gốc**: *DeepFire: A Novel Dataset and Deep Transfer Learning Benchmark for Forest Fire Detection* (A. Khan, B. Hassan, S. Khan, R. Ahmed, A. Adnan, 2022).
- **Phân phối**: Kaggle (`alik05/forest-fire-dataset`), giấy phép **Creative Commons Attribution 4.0 International (CC BY 4.0)**.
- **Xử lý toàn vẹn**: 1.896 ảnh hợp lệ sau khi loại bỏ ảnh trùng lặp tuyệt đối và cách ly các cụm ảnh tương đồng giữa các tập dữ liệu.

---

## Tác giả & Liên hệ
- **Sinh viên thực hiện**: Cáp Phạm Đình Thăng
- **Môn học**: Máy học (Machine Learning)
- **Kho lưu trữ GitHub**: [https://github.com/barackvn/MayHoc](https://github.com/barackvn/MayHoc)
