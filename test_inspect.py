import cv2
import joblib
import numpy as np
from skimage.feature import hog

import sys
default_path = r"C:/Users/Admin/.gemini/antigravity-ide/brain/ea74be19-02e3-41d6-8acb-6acc1725df1a/.user_uploaded/media_1789655740932.png"
img_path = sys.argv[1] if len(sys.argv) > 1 else default_path
img = cv2.imread(img_path)
if img is None:
    print(f"Cannot load image from: {img_path}")
    print("Usage: python test_inspect.py <path_to_image.jpg>")
    sys.exit(1)
print("Image loaded:", True, "shape:", img.shape)

resized = cv2.resize(img, (96, 96))
hsv = cv2.cvtColor(resized, cv2.COLOR_BGR2HSV)
hh = np.histogram(hsv[:, :, 0], bins=32, range=(0, 180))[0] / (96 * 96)
hs = np.histogram(hsv[:, :, 1], bins=16, range=(0, 256))[0] / (96 * 96)
hv = np.histogram(hsv[:, :, 2], bins=16, range=(0, 256))[0] / (96 * 96)
hist_feat = np.concatenate([hh, hs, hv])

gray = cv2.cvtColor(resized, cv2.COLOR_BGR2GRAY)
hog_feat = hog(gray, orientations=8, pixels_per_cell=(16, 16), cells_per_block=(2, 2), visualize=False)
raw_feat = np.concatenate([hist_feat, hog_feat]).reshape(1, -1)

import os
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
scaler = joblib.load(os.path.join(BASE_DIR, "models", "scaler.joblib"))
pca = joblib.load(os.path.join(BASE_DIR, "models", "pca.joblib"))
feat_scaled = scaler.transform(raw_feat)
feat_pca = pca.transform(feat_scaled)

print("-" * 60)
for name in ["Logistic_Regression", "KNN", "SVM", "Random_Forest"]:
    m = joblib.load(os.path.join(BASE_DIR, "models", f"{name}.joblib"))
    pred = int(m.predict(feat_pca)[0])
    label = "CHAY (Fire)" if pred == 1 else "KHONG CHAY (No Fire)"
    
    prob_str = "N/A"
    if hasattr(m, "predict_proba"):
        p = m.predict_proba(feat_pca)[0]
        prob_str = f"P(Fire)={p[1]*100:.2f}%"
        
    dec_str = "N/A"
    if hasattr(m, "decision_function"):
        d = m.decision_function(feat_pca)[0]
        dec_str = f"score={d:.4f}"
        
    print(f"{name:22s} -> {label:20s} | {prob_str:18s} | {dec_str}")
print("-" * 60)
