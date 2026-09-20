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
from fastapi.responses import JSONResponse, FileResponse
from pydantic import BaseModel
from PIL import Image, ImageOps
import numpy as np
from joblib import load

BACKEND_DIR = Path(__file__).resolve().parent
ROOT_DIR = BACKEND_DIR.parent

if str(ROOT_DIR / 'src') not in sys.path:
    sys.path.insert(0, str(ROOT_DIR / 'src'))

from experiment import feature, rgb2gray, SIZE, LABELS
from skimage.color import rgb2hsv
from skimage.feature import hog

app = FastAPI(
    title="Forest Fire ML Guard Backend API",
    description="Backend API phục vụ phân loại ảnh cháy rừng bằng 4 mô hình Machine Learning",
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
        "color": "red",
        "tags": ["LINEAR", "LBFGS", "PCA-231"],
        "params": "C = 1 | solver = 'lbfgs' | max_iter = 3000",
        "eval_type": "warning",
        "eval_title": "Baseline tuyến tính mạnh",
        "eval_desc": "Phân loại bằng hàm sigmoid trên tổ hợp tuyến tính 231 thành phần PCA."
    },
    "knn": {
        "key": "KNN",
        "file": "KNN.joblib",
        "name": "K-Nearest Neighbors (KNN)",
        "num": "2",
        "f1_val": "0.715",
        "f1_test": "0.676",
        "acc_test": "74.47%",
        "color": "blue",
        "tags": ["KNN-3", "UNIFORM", "EUCLIDEAN"],
        "params": "k = 3 | weights = 'uniform' | Euclidean",
        "eval_type": "info",
        "eval_title": "Cảnh báo: Bỏ sót nhiều (Recall thấp)",
        "eval_desc": "Khoảng cách Euclidean bị bão hòa trong không gian đa chiều, bỏ sót 46.8% vụ cháy."
    },
    "svm": {
        "key": "SVM",
        "file": "SVM.joblib",
        "name": "👑 SVM (Kernel RBF - Đề xuất SOTA)",
        "num": "3",
        "f1_val": "0.942",
        "f1_test": "0.940",
        "acc_test": "93.95%",
        "color": "green",
        "is_sota": True,
        "tags": ["SVM-RBF", "C=10", "RECALL: 95.3%", "SOTA BEST"],
        "params": "C = 10 | kernel = 'rbf' | gamma = 'scale'",
        "eval_type": "success",
        "eval_title": "Đề xuất SOTA Biên Cực Đại",
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
        "tags": ["FOREST-150", "BAGGING", "OVERFIT"],
        "params": "150 cây | max_depth = None | min_samples_leaf = 1",
        "eval_type": "info",
        "eval_title": "Học quá khớp (Overfitting nhẹ)",
        "eval_desc": "Biến đổi PCA làm mất tính độc lập đơn biến của các cây quyết định."
    }
}

LOADED_MODELS = {}
print("Loading 4 trained Machine Learning models into memory...", flush=True)
for alias, cfg in MODEL_CONFIGS.items():
    model_path = ROOT_DIR / "models" / cfg["file"]
    if model_path.exists():
        LOADED_MODELS[alias] = load(model_path)
        print(f"  -> Loaded {cfg['name']} from {cfg['file']}")
    else:
        print(f"  -> WARNING: File {model_path} not found!")

SAMPLE_DIR = ROOT_DIR / "data" / "raw" / "Forest Fire Dataset"
SAMPLE_PRESETS = [
    {
        "id": "sample_1",
        "name": "Mẫu 1",
        "label_text": "Mẫu 1 (Cháy rõ)",
        "desc": "Lửa lớn bùng phát dữ dội trong đêm",
        "file": "Testing/fire_0002.jpg",
        "true_class": "Cháy"
    },
    {
        "id": "sample_2",
        "name": "Mẫu 2",
        "label_text": "Mẫu 2 (Khói dày)",
        "desc": "Cột khói trắng đặc che khuất tán rừng",
        "file": "Testing/fire_0015.jpg",
        "true_class": "Cháy"
    },
    {
        "id": "sample_3",
        "name": "Mẫu 3",
        "label_text": "Mẫu 3 (Rừng xanh)",
        "desc": "Phong cảnh rừng bình yên nắng nhẹ",
        "file": "Testing/nofire_0006.jpg",
        "true_class": "Không cháy"
    },
    {
        "id": "sample_4",
        "name": "Mẫu 4",
        "label_text": "Mẫu 4 (Núi đá gắt)",
        "desc": "Vách đá và bầu trời sáng chói",
        "file": "Testing/nofire_0012.jpg",
        "true_class": "Không cháy"
    },
    {
        "id": "sample_5",
        "name": "Mẫu 5",
        "label_text": "Mẫu 5 (Lá vàng thu)",
        "desc": "Tán lá vàng đỏ dễ gây báo nhầm",
        "file": "Testing/nofire_0032.jpg",
        "true_class": "Không cháy"
    }
]

def analyze_image_properties(im: Image.Image):
    im_rgb = ImageOps.exif_transpose(im).convert('RGB')
    orig_w, orig_h = im_rgb.size
    im_resized = im_rgb.resize((SIZE, SIZE))
    rgb_arr = np.asarray(im_resized, dtype=np.float32) / 255.0
    gray_arr = rgb2gray(rgb_arr)
    
    brightness = float(np.mean(gray_arr))
    gray_255 = (gray_arr * 255).astype(np.float32)
    laplacian_kernel = np.array([[0, 1, 0], [1, -4, 1], [0, 1, 0]], dtype=np.float32)
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
    t_start = time.perf_counter()
    im_rgb = ImageOps.exif_transpose(im).convert('RGB')
    
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
        t_infer = (time.perf_counter() - t0) * 1000.0
        
        proba_chay = 0.5
        if hasattr(model, 'predict_proba'):
            p = model.predict_proba(feat_vector)[0]
            proba_chay = float(p[1])
        elif hasattr(model, 'decision_function'):
            score = float(model.decision_function(feat_vector)[0])
            proba_chay = float(1.0 / (1.0 + np.exp(-score)))
            
        is_fire = (pred_label == 1)
        conf = round(proba_chay * 100.0 if is_fire else (1.0 - proba_chay) * 100.0, 1)
        
        # Text display matching screenshot format
        masked_text = "🔥 ĐÁM CHÁY XUẤT HIỆN TRONG KHUNG HÌNH" if is_fire else "🌲 KHÔNG PHÁT HIỆN DẤU HIỆU CHÁY (AN TOÀN)"
        
        res_item = {
            "alias": alias,
            "key": cfg["key"],
            "name": cfg["name"],
            "num": cfg["num"],
            "color": cfg["color"],
            "is_sota": cfg.get("is_sota", False),
            "is_fire": is_fire,
            "label": pred_label,
            "class_name": "Cháy" if is_fire else "Không cháy",
            "confidence": conf,
            "prob_fire": round(proba_chay * 100.0, 1),
            "latency_ms": round(t_infer, 1),
            "f1_val": cfg["f1_val"],
            "f1_test": cfg["f1_test"],
            "acc_test": cfg["acc_test"],
            "tags": cfg["tags"],
            "params": cfg["params"],
            "masked_text": masked_text,
            "eval_type": cfg["eval_type"],
            "eval_title": cfg["eval_title"],
            "eval_desc": cfg["eval_desc"]
        }
        model_results.append(res_item)
        
    total_time = round(time.perf_counter() - t_start, 2)
    
    buf_preview = io.BytesIO()
    im_rgb.save(buf_preview, format='JPEG', quality=85)
    img_b64 = "data:image/jpeg;base64," + base64.b64encode(buf_preview.getvalue()).decode('utf-8')
    
    return {
        "total_latency_seconds": total_time,
        "image_properties": props,
        "models": model_results,
        "preview_image": img_b64
    }

@app.get("/api/health")
def health_check():
    return {
        "status": "online",
        "models_loaded": len(LOADED_MODELS),
        "models": list(LOADED_MODELS.keys())
    }

@app.get("/api/samples")
def get_samples():
    return {"samples": SAMPLE_PRESETS}

@app.get("/api/sample_image/{sample_id}")
def get_sample_image(sample_id: str):
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
    try:
        if file and file.filename:
            contents = await file.read()
            im = Image.open(io.BytesIO(contents))
        elif sample_id:
            target = next((s for s in SAMPLE_PRESETS if s["id"] == sample_id), None)
            if not target:
                raise HTTPException(status_code=400, detail="Mẫu không hợp lệ")
            im = Image.open(SAMPLE_DIR / target["file"])
        else:
            raise HTTPException(status_code=400, detail="Vui lòng cung cấp file ảnh hoặc sample_id")
        
        result = run_all_models(im)
        return JSONResponse(result)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/random_test")
def get_random_test_image():
    test_files = list((SAMPLE_DIR / "Testing").rglob("*.jpg"))
    if not test_files:
        raise HTTPException(status_code=404, detail="Không tìm thấy tập Testing")
    chosen = random.choice(test_files)
    im = Image.open(chosen)
    result = run_all_models(im)
    result["filename"] = chosen.name
    result["true_class"] = "Cháy" if "fire_" in chosen.name and "nofire" not in chosen.name else "Không cháy"
    return JSONResponse(result)

if __name__ == '__main__':
    import uvicorn
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
