from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from typing import List, Optional
import uvicorn
import os
import sys

# Thêm core vào path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from core.predictor import SentimentPredictor
from core.analytics import generate_simulated_timeline, predict_trend

app = FastAPI(title="Vietnamese Sentiment AI API")

# Cấu hình CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Khởi tạo predictor
predictor = SentimentPredictor()

# "Database" tạm thời trong bộ nhớ
history = []

class AnalyzeRequest(BaseModel):
    text: str

@app.get("/api/health")
async def health():
    return {"status": "ok", "model": "PhoBERT-Emotion"}

@app.post("/api/analyze")
async def analyze(request: AnalyzeRequest):
    if not request.text:
        raise HTTPException(status_code=400, detail="Text is empty")
    
    result = predictor.predict(request.text)
    
    # Lưu vào history
    history.insert(0, {
        "text": request.text,
        "result": result,
        "timestamp": os.popen("date /t").read().strip() 
    })
    
    return result

from fastapi import UploadFile, File
import pandas as pd
import io

@app.post("/api/analyze-file")
async def analyze_file(file: UploadFile = File(...)):
    if not file.filename.endswith(('.csv', '.txt')):
        raise HTTPException(status_code=400, detail="Only .csv and .txt files are supported")
    
    content = await file.read()
    results = []
    
    try:
        if file.filename.endswith('.csv'):
            df = pd.read_csv(io.BytesIO(content))
            # Tìm cột chứa văn bản
            text_col = None
            for col in ['text', 'comment', 'nội dung', 'content', 'message']:
                if col in df.columns:
                    text_col = col
                    break
            
            if text_col is None:
                # Nếu không tìm thấy cột tên chuẩn, lấy cột đầu tiên có kiểu string
                text_col = df.columns[0]
            
            texts = df[text_col].astype(str).tolist()
        else:
            # TXT file: Doc tung dong
            texts = content.decode('utf-8').splitlines()
            texts = [t.strip() for t in texts if t.strip()]

        # Xử lý hàng loạt (giới hạn 100 câu để tránh quá tải local)
        for t in texts[:100]:
            res = predictor.predict(t)
            results.append({
                "text": t,
                "top_emotion": res["top_emotion"],
                "confidence": res["confidence"],
                "is_long_text": res.get("is_long_text", False)
            })
            
            # Lưu vào history mẫu (chỉ lưu 5 câu đầu của file vào history chính)
            if len(results) <= 5:
                history.insert(0, {
                    "text": t,
                    "result": res,
                    "timestamp": "Batch Upload"
                })

        return {
            "filename": file.filename,
            "total": len(texts),
            "processed": len(results),
            "results": results
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing file: {str(e)}")

import json

def load_samples():
    current_dir = os.path.dirname(os.path.abspath(__file__))
    root_dir = os.path.dirname(current_dir)
    sample_path = os.path.join(root_dir, "data/social_media_samples.json")
    try:
        with open(sample_path, "r", encoding="utf-8") as f:
            return json.load(f)
    except:
        return [{"text": "Mẫu mặc định", "emotion": "Other"}]

@app.get("/api/samples")
async def get_samples():
    return load_samples()

@app.get("/api/keywords")
async def get_keywords():
    samples = load_samples()
    from core.lexicon import get_all_keywords
    lexicon = get_all_keywords()
    
    counts = {}
    for s in samples:
        words = predictor.tokenizer.tokenize(s["text"].lower())
        for w in words:
            if w in lexicon:
                counts[w] = counts.get(w, 0) + 1
    
    # Sắp xếp lấy Top 10
    top_keywords = sorted(counts.items(), key=lambda x: x[1], reverse=True)[:10]
    return [{"word": k, "count": v} for k, v in top_keywords]

@app.get("/api/trend")
async def get_trend():
    samples = load_samples()
    from core.analytics import generate_simulated_timeline, forecast_psi
    
    sample_comments = [s["text"] for s in samples]
    timeline = generate_simulated_timeline(predictor, sample_comments)
    
    # Gom nhóm theo ngày để tính PSI trung bình lịch sử
    daily_psi = {}
    for entry in timeline:
        day = entry["timestamp"][:10]
        if day not in daily_psi: daily_psi[day] = []
        daily_psi[day].append(entry["psi"])
    
    sorted_days = sorted(daily_psi.keys())
    historical_values = [sum(daily_psi[d])/len(daily_psi[d]) for d in sorted_days]
    
    # Dự báo 3 ngày tiếp theo
    forecast_values = forecast_psi(historical_values, days=3)
    
    return {
        "labels": sorted_days,
        "values": historical_values,
        "forecast": forecast_values,
        "trend": "Rising" if historical_values[-1] > historical_values[0] else "Falling"
    }

# Mount frontend static files
current_dir = os.path.dirname(os.path.abspath(__file__))
root_dir = os.path.dirname(current_dir)
frontend_path = os.path.join(root_dir, "frontend")

if os.path.exists(frontend_path):
    app.mount("/", StaticFiles(directory=frontend_path, html=True), name="frontend")
else:
    print(f"WARNING: Frontend path not found at {frontend_path}")

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
