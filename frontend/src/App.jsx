import React, { useState, useEffect } from 'react';
import {
  Flame, FileText, Database, Cpu, TrendingUp,
  Search, Download, CheckCircle2, AlertTriangle,
  RefreshCw, Info, Image as ImageIcon, Shield,
  Layers, HelpCircle, Activity, Sparkles
} from 'lucide-react';
import './App.css';

const API_BASE = 'http://127.0.0.1:8000';

const QUICK_SAMPLES = [
  { id: 'sample_1', label: 'Mẫu 1', name: 'Mẫu 1 (Cháy rõ)', desc: 'Ngọn lửa bùng phát lớn trong đêm' },
  { id: 'sample_2', label: 'Mẫu 2', name: 'Mẫu 2 (Khói dày)', desc: 'Cột khói trắng che khuất tán rừng' },
  { id: 'sample_3', label: 'Mẫu 3', name: 'Mẫu 3 (Rừng xanh)', desc: 'Phong cảnh rừng bình yên nắng nhẹ' },
  { id: 'sample_4', label: 'Mẫu 4', name: 'Mẫu 4 (Núi đá gắt)', desc: 'Vách đá và bầu trời sáng chói' },
  { id: 'sample_5', label: 'Mẫu 5', name: 'Mẫu 5 (Lá vàng thu)', desc: 'Tán lá vàng đỏ dễ gây báo nhầm' }
];

// Dữ liệu mẫu sẵn sàng để hiển thị tức thì ngay khi mở trang web
const INITIAL_DATA = {
  total_latency_seconds: 0.06,
  preview_image: `${API_BASE}/api/sample_image/sample_1`,
  image_properties: {
    width: 250,
    height: 250,
    brightness: 0.339,
    sharpness: 1686.2,
    mean_r: 0.476,
    mean_g: 0.297,
    mean_b: 0.195
  },
  models: [
    {
      alias: "lr",
      key: "Logistic Regression",
      name: "Logistic Regression (Baseline)",
      num: "1",
      color: "red",
      is_sota: false,
      is_fire: true,
      confidence: 99.8,
      prob_fire: 99.8,
      latency_ms: 1.2,
      f1_val: "0.934",
      f1_test: "0.927",
      tags: ["LINEAR", "LBFGS", "PCA-231"],
      masked_text: "🔥 ĐÁM CHÁY XUẤT HIỆN TRONG KHUNG HÌNH",
      eval_title: "Baseline tuyến tính mạnh",
      eval_desc: "Phân loại bằng hàm sigmoid trên tổ hợp tuyến tính 231 thành phần PCA."
    },
    {
      alias: "knn",
      key: "KNN",
      name: "K-Nearest Neighbors (KNN)",
      num: "2",
      color: "blue",
      is_sota: false,
      is_fire: false,
      confidence: 66.7,
      prob_fire: 33.3,
      latency_ms: 2.5,
      f1_val: "0.715",
      f1_test: "0.676",
      tags: ["KNN-3", "UNIFORM", "EUCLIDEAN"],
      masked_text: "🌲 KHÔNG PHÁT HIỆN DẤU HIỆU CHÁY (AN TOÀN)",
      eval_title: "Cảnh báo: Bỏ sót nhiều (Recall thấp)",
      eval_desc: "Khoảng cách Euclidean bị bão hòa trong không gian đa chiều, bỏ sót 46.8% vụ cháy."
    },
    {
      alias: "svm",
      key: "SVM",
      name: "👑 SVM (Kernel RBF - Đề xuất SOTA)",
      num: "3",
      color: "green",
      is_sota: true,
      is_fire: true,
      confidence: 96.5,
      prob_fire: 96.5,
      latency_ms: 1.4,
      f1_val: "0.942",
      f1_test: "0.940",
      tags: ["SVM-RBF", "C=10", "RECALL: 95.3%", "SOTA BEST"],
      masked_text: "🔥 ĐÁM CHÁY XUẤT HIỆN TRONG KHUNG HÌNH",
      eval_title: "Đề xuất SOTA Biên Cực Đại",
      eval_desc: "Kernel RBF phân tách phi tuyến vượt trội, đạt Recall 95.26%, chỉ bỏ sót 9/190 ảnh test."
    },
    {
      alias: "rf",
      key: "Random Forest",
      name: "Random Forest (Ensemble Đa Cây)",
      num: "4",
      color: "purple",
      is_sota: false,
      is_fire: true,
      confidence: 88.0,
      prob_fire: 88.0,
      latency_ms: 12.8,
      f1_val: "0.865",
      f1_test: "0.875",
      tags: ["FOREST-150", "BAGGING", "OVERFIT"],
      masked_text: "🔥 ĐÁM CHÁY XUẤT HIỆN TRONG KHUNG HÌNH",
      eval_title: "Học quá khớp (Overfitting nhẹ)",
      eval_desc: "Biến đổi PCA làm mất tính độc lập đơn biến của các cây quyết định."
    }
  ]
};

export default function App() {
  const [activeNav, setActiveNav] = useState('predict');
  const [activeSample, setActiveSample] = useState('sample_1');
  const [currentFile, setCurrentFile] = useState(null);
  const [previewUrl, setPreviewUrl] = useState(`${API_BASE}/api/sample_image/sample_1`);
  
  const [showFeatures, setShowFeatures] = useState(true);
  const [showDetails, setShowDetails] = useState(false);
  const [compareAll, setCompareAll] = useState(true);
  
  const [loading, setLoading] = useState(false);
  const [resultsData, setResultsData] = useState(INITIAL_DATA);
  const [backendOnline, setBackendOnline] = useState(false);

  // Ping backend API status
  useEffect(() => {
    const checkHealth = async () => {
      try {
        const res = await fetch(`${API_BASE}/api/health`);
        if (res.ok) {
          setBackendOnline(true);
        } else {
          setBackendOnline(false);
        }
      } catch {
        setBackendOnline(false);
      }
    };
    checkHealth();
  }, []);

  // Handle File Upload
  const handleFileChange = (e) => {
    if (e.target.files && e.target.files[0]) {
      const file = e.target.files[0];
      setCurrentFile(file);
      setActiveSample(null);
      setPreviewUrl(URL.createObjectURL(file));
    }
  };

  // Select preset sample
  const handleSelectSample = (sampleId) => {
    setActiveSample(sampleId);
    setCurrentFile(null);
    setPreviewUrl(`${API_BASE}/api/sample_image/${sampleId}`);
  };

  // Run Prediction
  const handleAnalyze = async () => {
    setLoading(true);
    const formData = new FormData();
    if (currentFile) {
      formData.append('file', currentFile);
    } else if (activeSample) {
      formData.append('sample_id', activeSample);
    } else {
      formData.append('sample_id', 'sample_1');
    }

    try {
      const res = await fetch(`${API_BASE}/api/predict`, {
        method: 'POST',
        body: formData
      });

      if (res.ok) {
        const data = await res.json();
        setResultsData(data);
        if (data.preview_image) {
          setPreviewUrl(data.preview_image);
        }
        setBackendOnline(true);
      } else {
        alert('Lỗi phản hồi từ server backend');
      }
    } catch (err) {
      console.warn('API error, using cached demo data:', err);
    } finally {
      setLoading(false);
    }
  };

  // Random Test
  const handleRandomTest = async () => {
    setLoading(true);
    try {
      const res = await fetch(`${API_BASE}/api/random_test`);
      if (res.ok) {
        const data = await res.json();
        setResultsData(data);
        if (data.preview_image) {
          setPreviewUrl(data.preview_image);
        }
        setActiveSample(null);
        setCurrentFile(null);
        setBackendOnline(true);
      }
    } catch (err) {
      alert('Không thể kết nối API random test');
    } finally {
      setLoading(false);
    }
  };

  // Download JSON
  const handleDownloadJSON = () => {
    const jsonStr = JSON.stringify(resultsData, null, 2);
    const blob = new Blob([jsonStr], { type: 'application/json' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = `ket_qua_phan_tich_chay_rung_${Date.now()}.json`;
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
  };

  return (
    <div className="app-container">
      {/* SIDEBAR THEO PHONG CÁCH ViHOS */}
      <aside className="sidebar">
        <div>
          <div className="brand-header">
            <div className="brand-icon-box">
              <Flame size={24} />
            </div>
            <div>
              <div className="brand-title">DeepFire Guard</div>
              <div className="brand-subtitle">Học Máy Phân Loại Ảnh</div>
            </div>
          </div>

          <nav className="nav-menu">
            <button
              className={`nav-item ${activeNav === 'predict' ? 'active' : ''}`}
              onClick={() => setActiveNav('predict')}
            >
              <Search size={18} /> Thử nghiệm mô hình
            </button>
            <button
              className={`nav-item ${activeNav === 'eda' ? 'active' : ''}`}
              onClick={() => setActiveNav('eda')}
            >
              <Database size={18} /> Phân tích dữ liệu (EDA)
            </button>
            <button
              className={`nav-item ${activeNav === 'features' ? 'active' : ''}`}
              onClick={() => setActiveNav('features')}
            >
              <Layers size={18} /> Đặc trưng (HSV + HOG)
            </button>
            <button
              className={`nav-item ${activeNav === 'benchmark' ? 'active' : ''}`}
              onClick={() => setActiveNav('benchmark')}
            >
              <TrendingUp size={18} /> Bảng chuẩn Benchmark
            </button>
            <button
              className={`nav-item ${activeNav === 'docs' ? 'active' : ''}`}
              onClick={() => setActiveNav('docs')}
            >
              <FileText size={18} /> Báo cáo môn học
            </button>
          </nav>
        </div>

        <div className="sidebar-footer">
          <div className="server-status-pill">
            <span style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
              <span className={`status-indicator ${backendOnline ? 'online' : 'offline'}`}></span>
              Backend API (Port 8000)
            </span>
            <span style={{ fontWeight: 600, color: backendOnline ? '#16A34A' : '#DC2626' }}>
              {backendOnline ? 'Online' : 'Offline'}
            </span>
          </div>
          <div style={{ fontSize: '0.72rem', color: '#94A3B8', textAlign: 'center' }}>
            UIT - ĐHQG TP.HCM | Học kỳ II 2025-2026
          </div>
        </div>
      </aside>

      {/* MAIN CONTENT AREA */}
      <main className="main-content">
        
        {/* TOP STATUS BAR */}
        <div className="top-status-bar">
          <div className="status-left">
            <Shield size={20} color="#2563EB" />
            <span>Hệ thống phân loại ảnh cháy rừng — Đồ án môn học Máy học</span>
          </div>
          <div className="status-badges">
            <span className="pill-badge pill-uit">UIT Benchmark</span>
            <span className="pill-badge pill-sota">SVM RBF: F1 94.03%</span>
          </div>
        </div>

        {/* INPUT CARD (GIỐNG HỆT GIAO DIỆN HÌNH ẢNH MẪU) */}
        <section className="white-card">
          <div className="card-title-row">
            <ImageIcon size={20} className="card-title-icon" />
            <span>Nhập ảnh cần phân tích</span>
          </div>

          <div className="card-body-padded">
            {/* DROPZONE UPLOAD & PREVIEW */}
            <div
              className="dropzone-box"
              onClick={() => document.getElementById('imageFileInput').click()}
            >
              <input
                type="file"
                id="imageFileInput"
                accept="image/jpeg,image/png,image/jpg"
                style={{ display: 'none' }}
                onChange={handleFileChange}
              />

              {previewUrl ? (
                <div className="dropzone-preview-box">
                  <img src={previewUrl} alt="Preview ảnh phân tích" />
                  <div className="dropzone-sub-text">Bấm vào ảnh để chọn tệp hình ảnh khác từ máy tính</div>
                </div>
              ) : (
                <div className="dropzone-inner-empty">
                  <ImageIcon size={44} color="#94A3B8" />
                  <div className="dropzone-main-text">
                    Kéo thả ảnh vào đây hoặc <span className="dropzone-link">bấm để chọn ảnh từ máy</span>
                  </div>
                  <div className="dropzone-sub-text">Hỗ trợ JPG, PNG, JPEG (ảnh chụp rừng, khói, lửa thực địa)</div>
                </div>
              )}
            </div>

            {/* VÍ DỤ THỬ NHANH (MẪU 1 -> MẪU 5) */}
            <div className="quick-samples-row">
              <span className="quick-label">Ví dụ thử nhanh:</span>
              <div className="sample-btns-group">
                {QUICK_SAMPLES.map(s => (
                  <button
                    key={s.id}
                    className={`sample-btn ${activeSample === s.id ? 'active' : ''}`}
                    onClick={() => handleSelectSample(s.id)}
                  >
                    {s.label}
                  </button>
                ))}
                <button
                  className="sample-btn sample-btn-random"
                  onClick={handleRandomTest}
                >
                  🎲 Ngẫu nhiên Test
                </button>
              </div>
            </div>

            {/* ACTION CHECKBOXES & BUTTON */}
            <div className="actions-bar">
              <div className="checkboxes-group">
                <label className="cb-label">
                  <input
                    type="checkbox"
                    checked={showFeatures}
                    onChange={(e) => setShowFeatures(e.target.checked)}
                  />
                  <span>Tự động trích đặc trưng (HSV + HOG)</span>
                </label>
                <label className="cb-label">
                  <input
                    type="checkbox"
                    checked={showDetails}
                    onChange={(e) => setShowDetails(e.target.checked)}
                  />
                  <span>Hiển thị thông số chi tiết</span>
                </label>
                <label className="cb-label">
                  <input
                    type="checkbox"
                    checked={compareAll}
                    onChange={(e) => setCompareAll(e.target.checked)}
                  />
                  <span>So sánh tất cả mô hình</span>
                </label>
              </div>

              <div className="actions-right">
                <span className="counter-tag">96×96 px | 864 đặc trưng</span>
                <button
                  className="btn-submit"
                  onClick={handleAnalyze}
                  disabled={loading}
                >
                  {loading ? <RefreshCw size={16} className="spin" /> : <Search size={16} />}
                  <span>Phân tích</span>
                </button>
              </div>
            </div>
          </div>
        </section>

        {/* RESULTS SECTION: KẾT QUẢ SO SÁNH ĐỒNG THỜI 4 MÔ HÌNH */}
        <section>
          <div className="results-header-bar">
            <div className="results-title">
              <TrendingUp size={22} color="#2563EB" />
              <span>Kết quả so sánh đồng thời 4 mô hình</span>
            </div>
            <div className="results-meta-actions">
              <span className="latency-badge">
                ⏱ Thời gian xử lý: {resultsData.total_latency_seconds} giây
              </span>
              <button
                className="btn-download-outline"
                onClick={handleDownloadJSON}
              >
                <Download size={14} /> Tải báo cáo
              </button>
            </div>
          </div>

          {/* 4 MODEL CARDS SIDE BY SIDE */}
          <div className="models-grid-4" style={{ marginTop: '16px' }}>
            {resultsData.models.map(m => {
              let badgeColor = 'badge-blue';
              if (m.num === '1') badgeColor = 'badge-red';
              if (m.num === '2') badgeColor = 'badge-blue';
              if (m.num === '3') badgeColor = 'badge-green';
              if (m.num === '4') badgeColor = 'badge-purple';

              return (
                <div
                  key={m.alias}
                  className={`result-model-card ${m.is_sota ? 'sota-border' : ''}`}
                >
                  {/* Card Header */}
                  <div className="model-head-row">
                    <div className="model-head-left">
                      <div className={`badge-number ${badgeColor}`}>{m.num}</div>
                      <div className="model-head-title">{m.name}</div>
                    </div>
                    <Info size={16} className="info-icon" />
                  </div>

                  {/* 3 Metrics Column */}
                  <div className="metrics-row-3">
                    <div className="metric-col-item">
                      <div className="m-label">Phát hiện</div>
                      <div className={`m-val ${m.is_fire ? 'text-danger' : 'green-text'}`}>
                        {m.is_fire ? 'Cháy' : 'An toàn'}
                      </div>
                    </div>
                    <div className="metric-col-item">
                      <div className="m-label">Thời gian xử lý</div>
                      <div className="m-val">{m.latency_ms} <span style={{ fontSize: '0.75rem', fontWeight: 500 }}>ms</span></div>
                    </div>
                    <div className="metric-col-item">
                      <div className="m-label">F1 (val)</div>
                      <div className={`m-val ${m.is_sota ? 'green-text' : ''}`}>{m.f1_val}</div>
                    </div>
                  </div>

                  {/* Detected Categories/Tags Row */}
                  <div>
                    <div style={{ fontSize: '0.72rem', color: '#64748B', fontWeight: 600, marginBottom: '6px' }}>
                      Các nhãn kỹ thuật:
                    </div>
                    <div className="detected-tags-row">
                      {m.tags.map(t => (
                        <span key={t} className={`tag-pill ${t.includes('SOTA') || t.includes('RECALL') ? 'tag-green' : t.includes('LINEAR') ? 'tag-red' : 'tag-blue'}`}>
                          {t}
                        </span>
                      ))}
                      <span className="tag-pill tag-gray">CONF: {m.confidence}%</span>
                    </div>
                  </div>

                  {/* Content Box (Masked text style) */}
                  <div className="masked-content-section">
                    <div className="masked-section-label">
                      <Sparkles size={14} color="#64748B" />
                      <span>Kết quả phân loại toàn ảnh:</span>
                    </div>
                    <div className={`masked-text-card ${m.is_fire ? 'fire-card' : 'nofire-card'}`}>
                      {m.masked_text}
                    </div>
                  </div>

                  {/* Evaluation Box */}
                  <div className="eval-note-box">
                    <strong>{m.eval_title}:</strong> {m.eval_desc}
                  </div>
                </div>
              );
            })}
          </div>
        </section>

        {/* THUỘC TÍNH ĐỊNH LƯỢNG ẢNH ĐANG XEM */}
        {resultsData.image_properties && (
          <section className="white-card">
            <div className="card-title-row">
              <Cpu size={20} className="card-title-icon" />
              <span>Chỉ số định lượng kỹ thuật của ảnh phân tích</span>
            </div>
            <div className="attrs-grid-4">
              <div className="attr-box">
                <div className="attr-val">
                  {resultsData.image_properties.width} × {resultsData.image_properties.height}
                </div>
                <div className="attr-title">Kích thước ảnh gốc</div>
                <div className="attr-sub">Tự động chuẩn hóa về 96×96 px</div>
              </div>
              <div className="attr-box">
                <div className="attr-val">{resultsData.image_properties.brightness}</div>
                <div className="attr-title">Độ sáng trung bình</div>
                <div className="attr-sub">Thang đo ảnh xám [0, 1]</div>
              </div>
              <div className="attr-box">
                <div className="attr-val">{resultsData.image_properties.sharpness}</div>
                <div className="attr-title">Độ sắc nét (Laplacian)</div>
                <div className="attr-sub">
                  {resultsData.image_properties.sharpness < 800 ? '⚠️ Ảnh có dấu hiệu mờ/khói' : '✅ Ảnh rõ nét chi tiết viền'}
                </div>
              </div>
              <div className="attr-box">
                <div className="attr-val">
                  R:{resultsData.image_properties.mean_r} G:{resultsData.image_properties.mean_g}
                </div>
                <div className="attr-title">Cường độ RGB trung bình</div>
                <div className="attr-sub">
                  {resultsData.image_properties.mean_r > resultsData.image_properties.mean_g ? 'Gam màu ấm (đỏ/cam)' : 'Gam màu lạnh/xanh'}
                </div>
              </div>
            </div>
          </section>
        )}

        {/* BENCHMARK TABLE */}
        <section className="white-card">
          <div className="card-title-row">
            <TrendingUp size={20} className="card-title-icon" />
            <span>Bảng chuẩn đối chứng kết quả 4 mô hình trên 380 ảnh Test</span>
          </div>
          <div style={{ padding: '0 20px 20px', overflowX: 'auto' }}>
            <table className="bench-table">
              <thead>
                <tr>
                  <th>STT</th>
                  <th>MÔ HÌNH HỌC MÁY</th>
                  <th>ACCURACY TEST</th>
                  <th>PRECISION CHÁY</th>
                  <th>RECALL CHÁY</th>
                  <th>F1-SCORE CHÁY</th>
                  <th>SỐ ẢNH BỎ SÓT (FN)</th>
                </tr>
              </thead>
              <tbody>
                <tr>
                  <td>1</td>
                  <td><strong>Logistic Regression (Baseline)</strong></td>
                  <td>92,63%</td>
                  <td>92,19%</td>
                  <td>93,16%</td>
                  <td>92,67%</td>
                  <td>13 / 190 ảnh</td>
                </tr>
                <tr>
                  <td>2</td>
                  <td><strong>K-Nearest Neighbors (KNN)</strong></td>
                  <td>74,47%</td>
                  <td>92,66%</td>
                  <td>53,16%</td>
                  <td>67,56%</td>
                  <td style={{ color: '#DC2626', fontWeight: 700 }}>89 / 190 ảnh (Bỏ sót nhiều)</td>
                </tr>
                <tr className="sota-row">
                  <td>3</td>
                  <td><strong>👑 SVM (Kernel RBF - Đề xuất SOTA)</strong></td>
                  <td style={{ color: '#16A34A', fontWeight: 700 }}>93,95%</td>
                  <td>92,82%</td>
                  <td style={{ color: '#16A34A', fontWeight: 700 }}>95,26%</td>
                  <td style={{ color: '#16A34A', fontWeight: 700 }}>94,03%</td>
                  <td style={{ color: '#16A34A', fontWeight: 700 }}>9 / 190 ảnh (Thấp nhất)</td>
                </tr>
                <tr>
                  <td>4</td>
                  <td><strong>Random Forest (Ensemble 150 Cây)</strong></td>
                  <td>87,63%</td>
                  <td>88,65%</td>
                  <td>86,32%</td>
                  <td>87,47%</td>
                  <td>26 / 190 ảnh</td>
                </tr>
              </tbody>
            </table>
          </div>
        </section>

      </main>
    </div>
  );
}
