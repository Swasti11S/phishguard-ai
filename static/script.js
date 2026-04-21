// script.js — PhishGuard AI
// Handles: tab switching, URL scanning, stats loading, result rendering

// ── DOM refs ─────────────────────────────────────
const urlInput    = document.getElementById('urlInput');
const scanBtn     = document.getElementById('scanBtn');
const clearBtn    = document.getElementById('clearBtn');
const loader      = document.getElementById('loader');
const resultPanel = document.getElementById('resultPanel');
const verdict     = document.getElementById('verdict');
const verdictIcon = document.getElementById('verdictIcon');
const verdictLabel= document.getElementById('verdictLabel');
const verdictUrl  = document.getElementById('verdictUrl');
const verdictConf = document.getElementById('verdictConfidence');
const featuresGrid= document.getElementById('featuresGrid');
const errorMsg    = document.getElementById('errorMsg');

// ── Tab switching ─────────────────────────────────
document.querySelectorAll('.tab').forEach(tab => {
  tab.addEventListener('click', () => {
    document.querySelectorAll('.tab').forEach(t => t.classList.remove('active'));
    document.querySelectorAll('.tab-panel').forEach(p => p.classList.remove('active'));
    tab.classList.add('active');
    document.getElementById('tab-' + tab.dataset.tab).classList.add('active');
    // Load stats when user opens the stats tab
    if (tab.dataset.tab === 'stats') loadStats();
  });
});

// ── Load model stats ──────────────────────────────
let statsLoaded = false;
async function loadStats() {
  if (statsLoaded) return;
  try {
    const res = await fetch('/stats');
    const d = await res.json();
    if (d.error) return;
    const pills = document.querySelectorAll('.metric-pill');
    const updates = [
      ['m-acc',   d.accuracy  + '%'],
      ['m-prec',  d.precision + '%'],
      ['m-rec',   d.recall    + '%'],
      ['m-f1',    d.f1_score  + '%'],
      ['m-auc',   d.roc_auc],
      ['m-total', d.total_samples.toLocaleString()]
    ];
    updates.forEach(([id, val], i) => {
      document.getElementById(id).textContent = val;
      pills[i].classList.remove('loading');
      pills[i].classList.add('loaded');
    });
    statsLoaded = true;
  } catch (e) { console.error('Stats load failed', e); }
}

// ── Scan events ───────────────────────────────────
scanBtn.addEventListener('click', analyzeURL);
urlInput.addEventListener('keydown', e => { if (e.key === 'Enter') analyzeURL(); });
urlInput.addEventListener('input', () => {
  clearBtn.classList.toggle('visible', urlInput.value.length > 0);
  hideResults();
});
clearBtn.addEventListener('click', () => {
  urlInput.value = '';
  clearBtn.classList.remove('visible');
  hideResults(); hideError();
  urlInput.focus();
});

// ── Fill example and auto-scan ────────────────────
function fillExample(url) {
  urlInput.value = url;
  clearBtn.classList.add('visible');
  hideResults(); hideError();
  urlInput.focus();
  analyzeURL();
}

// ── Main analyze function ─────────────────────────
async function analyzeURL() {
  const url = urlInput.value.trim();
  if (!url) { showError('Please enter a URL to analyze.'); return; }
  setLoading(true); hideResults(); hideError();
  try {
    const res = await fetch('/predict', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ url })
    });
    const data = await res.json();
    if (!res.ok || data.error) throw new Error(data.error || 'Server error.');
    renderResult(data);
  } catch (err) {
    showError(err.message || 'Could not connect to the server.');
  } finally {
    setLoading(false);
  }
}

// ── Render result ─────────────────────────────────
function renderResult(data) {
  const isPhishing = data.prediction === 1;
  verdict.className = 'verdict ' + (isPhishing ? 'phishing' : 'safe');
  verdictIcon.textContent = isPhishing ? '⚠️' : '✅';
  verdictLabel.textContent = isPhishing ? '⚠  PHISHING DETECTED' : '✓  SAFE URL';
  verdictUrl.textContent = data.url;
  verdictConf.innerHTML = `<span>${data.confidence}%</span>confidence`;

  featuresGrid.innerHTML = '';
  data.features.forEach(f => {
    const item = document.createElement('div');
    item.className = 'feature-item';
    const cls = getFeatureColor(f.name, f.value);
    item.innerHTML = `<span class="feature-name">${f.name}</span>
                      <span class="feature-value ${cls}">${formatValue(f.name, f.value)}</span>`;
    featuresGrid.appendChild(item);
  });
  resultPanel.classList.add('visible');
}

// ── Feature color coding ──────────────────────────
function getFeatureColor(name, value) {
  if (name === 'Uses HTTPS')      return value === 1 ? 'ok' : 'bad';
  if (name === 'Has IP Address')  return value === 1 ? 'bad' : 'ok';
  if (name === 'Has @ Symbol')    return value === 1 ? 'bad' : 'ok';
  if (name === 'Suspicious Keywords') {
    if (value === 0) return 'ok';
    if (value <= 2)  return 'neutral';
    return 'bad';
  }
  if (name === 'URL Length') {
    if (value < 60)  return 'ok';
    if (value < 100) return 'neutral';
    return 'bad';
  }
  if (name === 'Dot Count') {
    if (value <= 2) return 'ok';
    if (value <= 4) return 'neutral';
    return 'bad';
  }
  if (name === 'Hyphen Count') {
    if (value === 0) return 'ok';
    if (value <= 1)  return 'neutral';
    return 'bad';
  }
  if (name === 'Subdomain Count') {
    if (value === 0) return 'ok';
    if (value === 1) return 'neutral';
    return 'bad';
  }
  return 'neutral';
}

function formatValue(name, value) {
  if (name === 'Has IP Address' || name === 'Has @ Symbol')
    return value === 1 ? 'Yes ⚠' : 'No ✓';
  if (name === 'Uses HTTPS')
    return value === 1 ? 'Yes ✓' : 'No ✗';
  return value;
}

// ── UI helpers ────────────────────────────────────
function setLoading(active) {
  loader.classList.toggle('visible', active);
  scanBtn.disabled = active;
  scanBtn.querySelector('.btn-text').textContent = active ? 'Analyzing...' : 'Analyze URL';
}
function hideResults() { resultPanel.classList.remove('visible'); }
function showError(msg) { errorMsg.textContent = '⚠  ' + msg; errorMsg.classList.add('visible'); }
function hideError()    { errorMsg.classList.remove('visible'); }
