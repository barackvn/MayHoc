// Forest Fire ML Detector - Client Logic

let currentFile = null;
let currentSampleId = 'sample_1';
let lastAnalysisResult = null;

// DOM Elements
const dropzone = document.getElementById('dropzone');
const fileInput = document.getElementById('fileInput');
const dropzoneEmpty = document.getElementById('dropzoneEmpty');
const dropzonePreview = document.getElementById('dropzonePreview');
const previewImg = document.getElementById('previewImg');
const btnChangeImg = document.getElementById('btnChangeImg');
const btnAnalyze = document.getElementById('btnAnalyze');
const btnRandomTest = document.getElementById('btnRandomTest');
const btnDownloadReport = document.getElementById('btnDownloadReport');
const loadingState = document.getElementById('loadingState');
const resultsSection = document.getElementById('resultsSection');
const modelsGrid = document.getElementById('modelsGrid');
const propertiesGrid = document.getElementById('propertiesGrid');
const totalLatencyBadge = document.getElementById('totalLatencyBadge');
const samplesContainer = document.getElementById('samplesContainer');

// Drag & Drop
dropzone.addEventListener('click', (e) => {
  if (e.target !== btnChangeImg) {
    fileInput.click();
  }
});

dropzone.addEventListener('dragover', (e) => {
  e.preventDefault();
  dropzone.classList.add('dragover');
});

dropzone.addEventListener('dragleave', () => {
  dropzone.classList.remove('dragover');
});

dropzone.addEventListener('drop', (e) => {
  e.preventDefault();
  dropzone.classList.remove('dragover');
  if (e.dataTransfer.files && e.dataTransfer.files.length > 0) {
    handleFileSelect(e.dataTransfer.files[0]);
  }
});

fileInput.addEventListener('change', (e) => {
  if (e.target.files && e.target.files.length > 0) {
    handleFileSelect(e.target.files[0]);
  }
});

btnChangeImg.addEventListener('click', (e) => {
  e.stopPropagation();
  fileInput.click();
});

function handleFileSelect(file) {
  if (!file.type.match('image.*')) {
    alert('Vui lòng chọn một tệp hình ảnh (JPG, PNG).');
    return;
  }
  currentFile = file;
  currentSampleId = null;

  // Xóa active khỏi các nút mẫu
  document.querySelectorAll('.btn-sample').forEach(btn => btn.classList.remove('active'));

  const reader = new FileReader();
  reader.onload = (e) => {
    previewImg.src = e.target.result;
    dropzoneEmpty.style.display = 'none';
    dropzonePreview.style.display = 'block';
  };
  reader.readAsDataURL(file);
}

// Sample buttons
document.querySelectorAll('.btn-sample[data-sample]').forEach(btn => {
  btn.addEventListener('click', () => {
    document.querySelectorAll('.btn-sample').forEach(b => b.classList.remove('active'));
    btn.classList.add('active');
    
    currentSampleId = btn.getAttribute('data-sample');
    currentFile = null;
    
    // Hiển thị preview từ sample
    previewImg.src = `/api/sample_image/${currentSampleId}`;
    dropzoneEmpty.style.display = 'none';
    dropzonePreview.style.display = 'block';

    // Tự động phân tích ngay
    triggerAnalysis();
  });
});

// Random test
btnRandomTest.addEventListener('click', async () => {
  document.querySelectorAll('.btn-sample').forEach(b => b.classList.remove('active'));
  btnRandomTest.classList.add('active');
  
  showLoading(true);
  try {
    const res = await fetch('/api/random_test');
    if (!res.ok) throw new Error('Không thể tải ảnh ngẫu nhiên');
    const data = await res.json();
    
    currentFile = null;
    currentSampleId = null;
    
    previewImg.src = data.preview_image;
    dropzoneEmpty.style.display = 'none';
    dropzonePreview.style.display = 'block';
    
    renderResults(data);
  } catch (err) {
    alert('Lỗi: ' + err.message);
  } finally {
    showLoading(false);
  }
});

// Analyze Button
btnAnalyze.addEventListener('click', () => {
  triggerAnalysis();
});

async function triggerAnalysis() {
  if (!currentFile && !currentSampleId) {
    alert('Vui lòng chọn một ảnh tải lên hoặc bấm chọn một mẫu thử nghiệm.');
    return;
  }

  showLoading(true);

  const formData = new FormData();
  if (currentFile) {
    formData.append('file', currentFile);
  } else if (currentSampleId) {
    formData.append('sample_id', currentSampleId);
  }

  try {
    const res = await fetch('/api/predict', {
      method: 'POST',
      body: formData
    });

    if (!res.ok) {
      const err = await res.json();
      throw new Error(err.detail || 'Lỗi xử lý server');
    }

    const data = await res.json();
    renderResults(data);
  } catch (err) {
    alert('Lỗi phân tích: ' + err.message);
  } finally {
    showLoading(false);
  }
}

function showLoading(show) {
  if (show) {
    loadingState.style.display = 'block';
    resultsSection.style.display = 'none';
    btnAnalyze.disabled = true;
  } else {
    loadingState.style.display = 'none';
    btnAnalyze.disabled = false;
  }
}

function renderResults(data) {
  lastAnalysisResult = data;
  resultsSection.style.display = 'flex';
  
  // Update Latency Badge
  totalLatencyBadge.textContent = `⏱ Thời gian xử lý: ${data.total_latency_seconds} giây`;

  // Render 4 Model Cards
  modelsGrid.innerHTML = '';
  data.models.forEach(model => {
    const card = createModelCard(model);
    modelsGrid.appendChild(card);
  });

  // Render Properties
  renderProperties(data.image_properties);

  // Scroll to results smoothly
  resultsSection.scrollIntoView({ behavior: 'smooth', block: 'start' });
}

function createModelCard(m) {
  const card = document.createElement('div');
  card.className = `model-card ${m.is_sota ? 'is-sota' : ''}`;

  let numColorClass = 'num-blue';
  if (m.num === '1') numColorClass = 'num-red';
  else if (m.num === '2') numColorClass = 'num-blue';
  else if (m.num === '3') numColorClass = 'num-green';
  else if (m.num === '4') numColorClass = 'num-purple';

  const isFire = m.is_fire;
  const predBoxClass = isFire ? 'fire' : 'nofire';
  const predText = isFire ? '🔥 CHÁY RỪNG (FIRE)' : '🌲 AN TOÀN (NO FIRE)';

  card.innerHTML = `
    <div class="model-card-header">
      <div class="model-num-circle ${numColorClass}">${m.num}</div>
      <div class="model-name">${m.name}</div>
    </div>

    <div class="model-card-body">
      <!-- 3 Chỉ số đầu card -->
      <div class="stats-row">
        <div class="stat-item">
          <div class="stat-label">Độ tin cậy</div>
          <div class="stat-value ${m.is_sota ? 'highlight-green' : ''}">${m.confidence}%</div>
        </div>
        <div class="stat-item">
          <div class="stat-label">Thời gian</div>
          <div class="stat-value">${m.latency_ms} <span style="font-size: 11px;">ms</span></div>
        </div>
        <div class="stat-item">
          <div class="stat-label">F1 Validation</div>
          <div class="stat-value ${m.is_sota ? 'highlight-green' : ''}">${m.f1_val}</div>
        </div>
      </div>

      <!-- Khối nhãn kết quả dự đoán -->
      <div class="prediction-box ${predBoxClass}">
        <div class="prediction-title">Kết quả phân loại</div>
        <div class="prediction-status">${predText}</div>
        <div class="prediction-prob">Xác suất Cháy: ${m.prob_fire}%</div>
      </div>

      <!-- Đánh giá mô hình -->
      <div class="model-eval-box eval-${m.eval_type}">
        <div class="eval-title">${m.eval_title}</div>
        <div class="eval-desc">${m.eval_desc}</div>
      </div>

      <!-- Tham số kỹ thuật -->
      <div class="model-params-box">
        <strong>Tham số:</strong> ${m.params}
      </div>
    </div>
  `;

  return card;
}

function renderProperties(props) {
  propertiesGrid.innerHTML = `
    <div class="prop-box">
      <div class="prop-num">${props.width} × ${props.height}</div>
      <div class="prop-label">Kích thước ảnh gốc</div>
      <div class="prop-sub">Đã tự động resize về 96×96 px</div>
    </div>
    <div class="prop-box">
      <div class="prop-num">${props.brightness}</div>
      <div class="prop-label">Độ sáng trung bình</div>
      <div class="prop-sub">Thang chuẩn hóa ảnh xám [0, 1]</div>
    </div>
    <div class="prop-box">
      <div class="prop-num">${props.sharpness}</div>
      <div class="prop-label">Độ sắc nét (Laplacian)</div>
      <div class="prop-sub">${props.sharpness < 800 ? '⚠️ Ảnh có dấu hiệu mờ/khói' : '✅ Ảnh rõ nét chi tiết viền'}</div>
    </div>
    <div class="prop-box">
      <div class="prop-num">R:${props.mean_r} G:${props.mean_g} B:${props.mean_b}</div>
      <div class="prop-label">Cường độ RGB trung bình</div>
      <div class="prop-sub">${props.mean_r > props.mean_g ? 'Kênh Đỏ chiếm ưu thế (Gam ấm)' : 'Kênh Lục/Lam chiếm ưu thế'}</div>
    </div>
  `;
}

// Download JSON report
btnDownloadReport.addEventListener('click', () => {
  if (!lastAnalysisResult) return;
  const jsonStr = JSON.stringify(lastAnalysisResult, null, 2);
  const blob = new Blob([jsonStr], { type: 'application/json' });
  const url = URL.createObjectURL(blob);
  const a = document.createElement('a');
  a.href = url;
  a.download = `ket_qua_phan_tich_chay_rung_${Date.now()}.json`;
  document.body.appendChild(a);
  a.click();
  document.body.removeChild(a);
  URL.revokeObjectURL(url);
});

// Khởi chạy mặc định với Mẫu 1 khi trang vừa load
window.addEventListener('DOMContentLoaded', () => {
  const firstSampleBtn = document.querySelector('.btn-sample[data-sample="sample_1"]');
  if (firstSampleBtn) {
    firstSampleBtn.click();
  }
});
