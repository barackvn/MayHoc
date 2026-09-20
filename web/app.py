import os
import sys
import time
import io
import json
import base64
import random
import warnings
from pathlib import Path
from typing import Optional

warnings.filterwarnings('ignore')

# Đảm bảo stdout UTF-8 trên Windows
sys.stdout.reconfigure(encoding='utf-8')

from fastapi import FastAPI, File, UploadFile, Form, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse, JSONResponse, FileResponse
from pydantic import BaseModel
from PIL import Image, ImageOps
import numpy as np
from joblib import load

# Đảm bảo đường dẫn import src/experiment.py
WEB_DIR = Path(__file__).resolve().parent
ROOT_DIR = WEB_DIR.parent
STATIC_DIR = WEB_DIR / 'static'
STATIC_DIR.mkdir(parents=True, exist_ok=True)

if str(ROOT_DIR / 'src') not in sys.path:
    sys.path.insert(0, str(ROOT_DIR / 'src'))

from experiment import feature, rgb2gray, SIZE, LABELS

app = FastAPI(
    title="Forest Fire ML Detector",
    description="Hệ thống phân tích và so sánh 4 mô hình Machine Learning nhận diện cháy rừng",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Cấu hình 4 mô hình
MODEL_CONFIGS = {
    "lr": {
        "key": "Logistic Regression",
        "file": "Logistic_Regression.joblib",
        "name": "Logistic Regression (Baseline)",
        "num": "1",
        "f1_val": "0.934",
        "f1_test": "0.927",
        "acc_test": "92.63%",
        "color": "blue",
        "params": "C = 1 | solver = 'lbfgs' | PCA = 231 dims",
        "eval_type": "info",
        "eval_title": "Baseline tuyến tính mạnh",
        "eval_desc": "Phân loại bằng hàm sigmoid trên tổ hợp tuyến tính các đặc trưng PCA."
    },
    "knn": {
        "key": "KNN",
        "file": "KNN.joblib",
        "name": "K-Nearest Neighbors (KNN)",
        "num": "2",
        "f1_val": "0.715",
        "f1_test": "0.676",
        "acc_test": "74.47%",
        "color": "orange",
        "params": "k = 3 | weights = 'uniform' | Euclidean",
        "eval_type": "warning",
        "eval_title": "Cảnh báo: Bỏ sót nhiều (Recall thấp)",
        "eval_desc": "Khoảng cách Euclidean bị bão hòa trong không gian đa chiều, bỏ sót 46.8% số vụ cháy."
    },
    "svm": {
        "key": "SVM",
        "file": "SVM.joblib",
        "name": "👑 Support Vector Machine (Đề xuất tối ưu SOTA)",
        "num": "3",
        "f1_val": "0.942",
        "f1_test": "0.940",
        "acc_test": "93.95%",
        "color": "green",
        "is_sota": True,
        "params": "C = 10 | kernel = 'rbf' | gamma = 'scale'",
        "eval_type": "sota",
        "eval_title": "Mô hình tối ưu xuất sắc nhất",
        "eval_desc": "Kernel RBF phân tách phi tuyến vượt trội, đạt Recall 95.26%, chỉ bỏ sót 9/190 ảnh test."
    },
    "rf": {
        "key": "Random Forest",
        "file": "Random_Forest.joblib",
        "name": "Random Forest (Ensemble Đa Cây)",
        "num": "4",
        "f1_val": "0.865",
        "f1_test": "0.875",
        "acc_test": "87.63%",
        "color": "purple",
        "params": "150 cây | max_depth = None | min_samples_leaf = 1",
        "eval_type": "info",
        "eval_title": "Học quá khớp (Overfitting nhẹ)",
        "eval_desc": "Biến đổi PCA làm mất tính độc lập đơn biến của các cây quyết định."
    }
}

# Tải trước 4 mô hình vào bộ nhớ RAM
LOADED_MODELS = {}
print("Loading trained models into memory...", flush=True)
for alias, cfg in MODEL_CONFIGS.items():
    model_path = ROOT_DIR / "models" / cfg["file"]
    if model_path.exists():
        LOADED_MODELS[alias] = load(model_path)
        print(f"Loaded {cfg['name']} from {cfg['file']}")
    else:
        print(f"WARNING: Model file not found: {model_path}")

# Danh sách 5 ảnh mẫu đại diện cho các tình huống thực tế
SAMPLE_DIR = ROOT_DIR / "data" / "raw" / "Forest Fire Dataset"
SAMPLE_PRESETS = [
    {
        "id": "sample_1",
        "name": "Mẫu 1 (Cháy rõ)",
        "desc": "Lửa lớn bùng phát dữ dội trong đêm",
        "file": "Testing/fire_0002.jpg",
        "true_label": 1,
        "true_class": "Cháy"
    },
    {
        "id": "sample_2",
        "name": "Mẫu 2 (Khói dày)",
        "desc": "Cột khói trắng đặc che khuất tán rừng",
        "file": "Testing/fire_0015.jpg",
        "true_label": 1,
        "true_class": "Cháy"
    },
    {
        "id": "sample_3",
        "name": "Mẫu 3 (Rừng thông xanh)",
        "desc": "Phong cảnh rừng bình yên nắng nhẹ",
        "file": "Testing/nofire_0006.jpg",
        "true_label": 0,
        "true_class": "Không cháy"
    },
    {
        "id": "sample_4",
        "name": "Mẫu 4 (Núi đá gắt)",
        "desc": "Vách đá và bầu trời sáng chói",
        "file": "Testing/nofire_0012.jpg",
        "true_label": 0,
        "true_class": "Không cháy"
    },
    {
        "id": "sample_5",
        "name": "Mẫu 5 (Lá vàng mùa thu)",
        "desc": "Tán lá vàng đỏ dễ gây báo nhầm",
        "file": "Testing/nofire_0032.jpg",
        "true_label": 0,
        "true_class": "Không cháy"
    }
]

def analyze_image_properties(im: Image.Image):
    """Tính toán các chỉ số kỹ thuật ảnh: độ sáng, độ sắc nét Laplacian, RGB trung bình."""
    im_rgb = ImageOps.exif_transpose(im).convert('RGB')
    orig_w, orig_h = im_rgb.size
    
    # Resize tạm 96x96 để tính toán đồng nhất
    im_resized = im_rgb.resize((SIZE, SIZE))
    rgb_arr = np.asarray(im_resized, dtype=np.float32) / 255.0
    gray_arr = rgb2gray(rgb_arr)
    
    # Độ sáng trung bình [0, 1]
    brightness = float(np.mean(gray_arr))
    
    # Độ sắc nét (phương sai toán tử Laplacian 3x3)
    gray_255 = (gray_arr * 255).astype(np.float32)
    laplacian_kernel = np.array([[0, 1, 0], [1, -4, 1], [0, 1, 0]], dtype=np.float32)
    # Tích chập 2D đơn giản
    from scipy.signal import convolve2d
    lap = convolve2d(gray_255, laplacian_kernel, mode='valid')
    laplacian_var = float(np.var(lap))
    
    mean_r = float(np.mean(rgb_arr[:, :, 0]))
    mean_g = float(np.mean(rgb_arr[:, :, 1]))
    mean_b = float(np.mean(rgb_arr[:, :, 2]))
    
    return {
        "width": orig_w,
        "height": orig_h,
        "brightness": round(brightness, 3),
        "sharpness": round(laplacian_var, 1),
        "mean_r": round(mean_r, 3),
        "mean_g": round(mean_g, 3),
        "mean_b": round(mean_b, 3)
    }

def run_all_models(im: Image.Image):
    """Trích xuất đặc trưng và suy luận qua 4 mô hình."""
    # Lưu tạm ảnh vào buffer để hàm feature đọc
    t_start = time.perf_counter()
    im_rgb = ImageOps.exif_transpose(im).convert('RGB')
    
    # Tạo vector đặc trưng HSV + HOG (864 chiều)
    # Tận dụng hàm trích đặc trưng chuẩn của experiment.py
    buf = io.BytesIO()
    im_rgb.save(buf, format='JPEG')
    buf.seek(0)
    
    # Trích xuất đặc trưng từ file tạm hoặc trực tiếp
    # Tái tạo logic feature() trên PIL Image trực tiếp
    from skimage.color import rgb2hsv
    from skimage.feature import hog
    
    rgb = np.asarray(im_rgb.resize((SIZE, SIZE)), dtype=np.float32) / 255.0
    hsv = rgb2hsv(rgb)
    color_feat = np.concatenate([np.histogram(hsv[:, :, c], bins=b, range=(0, 1))[0] / (SIZE * SIZE) for c, b in enumerate([32, 16, 16])])
    
    gray = rgb2gray(rgb)
    hog_feat = hog(
        gray, orientations=8, pixels_per_cell=(16, 16),
        cells_per_block=(2, 2), block_norm='L2-Hys'
    )
    feat_vector = np.r_[color_feat, hog_feat].astype(np.float32)[None, :]
    
    props = analyze_image_properties(im)
    
    model_results = []
    for alias, cfg in MODEL_CONFIGS.items():
        if alias not in LOADED_MODELS:
            continue
        model = LOADED_MODELS[alias]
        t0 = time.perf_counter()
        pred_label = int(model.predict(feat_vector)[0])
        t_infer = (time.perf_counter() - t0) * 1000.0  # ms
        
        proba_chay = 0.5
        if hasattr(model, 'predict_proba'):
            p = model.predict_proba(feat_vector)[0]
            proba_chay = float(p[1])
        elif hasattr(model, 'decision_function'):
            score = float(model.decision_function(feat_vector)[0])
            proba_chay = float(1.0 / (1.0 + np.exp(-score)))
        
        is_fire = (pred_label == 1)
        res_item = {
            "alias": alias,
            "name": cfg["name"],
            "num": cfg["num"],
            "color": cfg["color"],
            "is_sota": cfg.get("is_sota", False),
            "label": pred_label,
            "class_name": "Cháy (Fire)" if is_fire else "Không cháy (No Fire)",
            "is_fire": is_fire,
            "confidence": round(proba_chay * 100.0 if is_fire else (1.0 - proba_chay) * 100.0, 1),
            "prob_fire": round(proba_chay * 100.0, 1),
            "latency_ms": round(t_infer, 1),
            "f1_val": cfg["f1_val"],
            "f1_test": cfg["f1_test"],
            "acc_test": cfg["acc_test"],
            "params": cfg["params"],
            "eval_type": cfg["eval_type"],
            "eval_title": cfg["eval_title"],
            "eval_desc": cfg["eval_desc"]
        }
        model_results.append(res_item)
        
    total_time = round(time.perf_counter() - t_start, 3)
    
    # Chuyển ảnh sang base64 data url để preview
    buf_preview = io.BytesIO()
    im_rgb.save(buf_preview, format='JPEG', quality=85)
    img_b64 = "data:image/jpeg;base64," + base64.b64encode(buf_preview.getvalue()).decode('utf-8')
    
    return {
        "total_latency_seconds": total_time,
        "image_properties": props,
        "models": model_results,
        "preview_image": img_b64
    }

@app.get("/api/samples")
def get_samples():
    """Lấy danh sách các ảnh mẫu thử nhanh."""
    return {"samples": SAMPLE_PRESETS}

@app.get("/api/sample_image/{sample_id}")
def get_sample_image(sample_id: str):
    """Phục vụ file ảnh mẫu."""
    for s in SAMPLE_PRESETS:
        if s["id"] == sample_id:
            p = SAMPLE_DIR / s["file"]
            if p.exists():
                return FileResponse(p, media_type="image/jpeg")
    raise HTTPException(status_code=404, detail="Sample not found")

@app.post("/api/predict")
async def predict_endpoint(
    file: Optional[UploadFile] = File(None),
    sample_id: Optional[str] = Form(None)
):
    """Dự đoán đồng thời trên cả 4 mô hình."""
    try:
        if file and file.filename:
            contents = await file.read()
            im = Image.open(io.BytesIO(contents))
        elif sample_id:
            target_preset = next((s for s in SAMPLE_PRESETS if s["id"] == sample_id), None)
            if not target_preset:
                raise HTTPException(status_code=400, detail="Không tìm thấy mẫu")
            p = SAMPLE_DIR / target_preset["file"]
            if not p.exists():
                raise HTTPException(status_code=404, detail=f"File mẫu {p} không tồn tại")
            im = Image.open(p)
        else:
            raise HTTPException(status_code=400, detail="Vui lòng tải lên một ảnh hoặc chọn một mẫu thử.")
        
        result = run_all_models(im)
        return JSONResponse(result)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Lỗi phân tích: {str(e)}")

@app.get("/api/random_test")
def get_random_test_image():
    """Lấy ngẫu nhiên một ảnh từ tập testing."""
    test_files = list((SAMPLE_DIR / "Testing").rglob("*.jpg"))
    if not test_files:
        raise HTTPException(status_code=404, detail="Không tìm thấy tập Testing")
    chosen = random.choice(test_files)
    im = Image.open(chosen)
    result = run_all_models(im)
    result["filename"] = chosen.name
    result["true_class"] = "Cháy" if "fire_" in chosen.name and "nofire" not in chosen.name else "Không cháy"
    return JSONResponse(result)

# Mount thư mục static
app.mount("/", StaticFiles(directory=str(STATIC_DIR), html=True), name="static")

if __name__ == '__main__':
    import uvicorn
    print("Khởi động server Web Demo tại: http://localhost:8000", flush=True)
    uvicorn.run("app:app", host="0.0.0.0", port=8000, reload=True)
