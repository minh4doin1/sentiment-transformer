let emotionChart = null;
let psiChart = null;
let distChart = null;

const EMOTION_MAP = {
    "Enjoyment": "😊",
    "Sadness": "😢",
    "Fear": "😨",
    "Anger": "😡",
    "Disgust": "🤢",
    "Surprise": "😲",
    "Other": "😐"
};

document.addEventListener('DOMContentLoaded', () => {
    initCharts();
    checkBackendStatus();

    document.getElementById('btn-analyze').addEventListener('click', analyzeText);
    document.getElementById('btn-batch').addEventListener('click', loadSamples);
    document.getElementById('btn-clear').addEventListener('click', () => {
        document.getElementById('text-input').value = '';
        document.getElementById('result-container').classList.add('hidden');
        document.getElementById('sample-area').classList.add('hidden');
    });
});

function initCharts() {
    Chart.defaults.color = '#94a3b8';
    
    // Emotion Radar Chart
    const ctxRadar = document.getElementById('emotionRadarChart').getContext('2d');
    emotionChart = new Chart(ctxRadar, {
        type: 'radar',
        data: {
            labels: Object.keys(EMOTION_MAP),
            datasets: [{
                label: 'Cường độ cảm xúc',
                data: [0, 0, 0, 0, 0, 0, 0],
                backgroundColor: 'rgba(99, 102, 241, 0.2)',
                borderColor: 'rgba(99, 102, 241, 1)',
                pointBackgroundColor: 'rgba(99, 102, 241, 1)'
            }]
        }
    });

    // PSI Line Chart
    const ctxLine = document.getElementById('psiLineChart').getContext('2d');
    psiChart = new Chart(ctxLine, {
        type: 'line',
        data: {
            labels: [],
            datasets: [
                {
                    label: 'Dữ liệu thực tế',
                    data: [],
                    borderColor: '#6366f1',
                    backgroundColor: 'rgba(99, 102, 241, 0.1)',
                    fill: true,
                    tension: 0.4
                },
                {
                    label: 'Dự báo xu hướng',
                    data: [],
                    borderColor: '#a5b4fc',
                    borderDash: [5, 5],
                    backgroundColor: 'transparent',
                    fill: false,
                    tension: 0.4
                }
            ]
        },
        options: { 
            scales: { y: { min: -1, max: 1 } },
            responsive: true,
            maintainAspectRatio: false
        }
    });

    // Emotion Distribution Bar Chart
    const ctxBar = document.getElementById('emotionDistChart').getContext('2d');
    distChart = new Chart(ctxBar, {
        type: 'bar',
        data: {
            labels: Object.keys(EMOTION_MAP),
            datasets: [{
                label: 'Số lượng câu mẫu',
                data: [0, 0, 0, 0, 0, 0, 0],
                backgroundColor: [
                    '#4ade80', '#60a5fa', '#a78bfa', '#f87171', '#fbbf24', '#f472b6', '#94a3b8'
                ]
            }]
        },
        options: {
            indexAxis: 'y',
            plugins: { legend: { display: false } }
        }
    });
}

async function loadSamples() {
    try {
        const response = await fetch('http://localhost:8000/api/samples');
        const samples = await response.json();
        renderSamples(samples);
        updateDistChart(samples);
        fetchKeywords(); 
        document.getElementById('sample-area').classList.remove('hidden');
        fetchTrends();
    } catch (err) {
        console.error("Error loading samples:", err);
    }
}

async function fetchKeywords() {
    try {
        const response = await fetch('http://localhost:8000/api/keywords');
        const keywords = await response.json();
        
        const list = document.getElementById('keyword-list');
        list.innerHTML = '';
        keywords.forEach(k => {
            const span = document.createElement('span');
            span.className = 'keyword-tag';
            span.style.fontSize = `${0.8 + k.count * 0.2}rem`;
            span.style.opacity = Math.min(1, 0.4 + k.count * 0.1);
            span.innerText = `${k.word} (${k.count})`;
            list.appendChild(span);
        });
    } catch (err) {
        console.error("Fetch keywords error:", err);
    }
}

function updateDistChart(samples) {
    const counts = {};
    Object.keys(EMOTION_MAP).forEach(l => counts[l] = 0);
    samples.forEach(s => {
        if (counts[s.emotion] !== undefined) counts[s.emotion]++;
    });
    
    distChart.data.datasets[0].data = Object.values(counts);
    distChart.update();
}

function showSection(sectionId) {
    document.querySelectorAll('.section').forEach(s => s.classList.remove('active'));
    document.querySelectorAll('nav li').forEach(l => l.classList.remove('active'));
    
    document.getElementById(`${sectionId}-section`).classList.add('active');
    const navItem = Array.from(document.querySelectorAll('nav li')).find(li => li.getAttribute('onclick').includes(sectionId));
    if (navItem) navItem.classList.add('active');

    if (sectionId === 'dashboard') {
        fetchTrends();
    }
}

async function analyzeText() {
    const text = document.getElementById('text-input').value.trim();
    if (!text) return alert("Vui lòng nhập văn bản!");

    document.getElementById('loader').classList.remove('hidden');
    
    try {
        const response = await fetch('http://localhost:8000/api/analyze', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ text })
        });
        const data = await response.json();
        displayResult(data);
    } catch (err) {
        console.error(err);
        alert("Lỗi kết nối với Backend! Đảm bảo server đang chạy.");
    } finally {
        document.getElementById('loader').classList.add('hidden');
    }
}

function displayResult(data) {
    document.getElementById('result-container').classList.remove('hidden');
    document.getElementById('emotion-label').innerText = data.top_emotion;
    document.getElementById('emotion-emoji').innerText = EMOTION_MAP[data.top_emotion] || '😐';
    document.getElementById('emotion-confidence').innerText = `${(data.confidence * 100).toFixed(1)}%`;

    const highlightsDiv = document.getElementById('emotion-highlights');
    highlightsDiv.innerHTML = '';
    if (data.highlights && data.highlights.length > 0) {
        data.highlights.forEach(word => {
            const span = document.createElement('span');
            span.className = `tag tag-${data.top_emotion.toLowerCase()}`;
            span.innerText = word;
            highlightsDiv.appendChild(span);
        });
    }

    emotionChart.data.datasets[0].data = Object.values(data.probabilities);
    emotionChart.update();
}

async function fetchTrends() {
    try {
        const response = await fetch('http://localhost:8000/api/trend');
        const data = await response.json();
        
        const labels = [...data.labels];
        const historical = [...data.values];
        const forecastData = new Array(historical.length - 1).fill(null);
        forecastData.push(historical[historical.length - 1]);
        forecastData.push(...data.forecast);
        
        for (let i = 1; i <= data.forecast.length; i++) {
            labels.push(`Dự báo +${i}d`);
        }

        psiChart.data.labels = labels;
        psiChart.data.datasets[0].data = historical;
        psiChart.data.datasets[1].data = forecastData;
        psiChart.update();
        
        document.getElementById('current-psi').innerText = historical[historical.length - 1].toFixed(2);
        document.getElementById('psi-trend-text').innerText = data.trend;
        document.getElementById('trend-desc').innerText = `Xu hướng dư luận đang có dấu hiệu: ${data.trend}`;
    } catch (err) {
        console.error("Trend data error:", err);
    }
}

function renderSamples(samples) {
    const list = document.getElementById('sample-list');
    list.innerHTML = '';
    samples.forEach(s => {
        const item = document.createElement('div');
        item.className = 'sample-item glass-card';
        item.innerText = s.text;
        item.onclick = () => {
            document.getElementById('text-input').value = s.text;
            analyzeText();
        };
        list.appendChild(item);
    });
}

function checkBackendStatus() {
    fetch('http://localhost:8000/api/health')
        .then(res => res.json())
        .then(data => {
            document.getElementById('device-status').innerText = 'Online';
        })
        .catch(() => {
            document.getElementById('device-status').innerText = 'Offline';
        });
}
