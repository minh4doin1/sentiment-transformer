import pandas as pd
import numpy as np
from datetime import datetime, timedelta

def calculate_psi(sentiments):
    """
    Tính toán Chỉ số Dư luận (PSI) dựa trên trọng số cường độ cảm xúc.
    Dải giá trị: [-1, 1]
    """
    weights = {
        "Enjoyment": 1.0,
        "Surprise": 0.3,
        "Sadness": -0.6,
        "Fear": -0.8,
        "Disgust": -1.2,
        "Anger": -1.5,
        "Other": 0
    }
    
    total = sum(sentiments.values())
    if total == 0: return 0
    
    weighted_sum = sum(sentiments.get(emo, 0) * weights.get(emo, 0) for emo in weights)
    
    # Chuẩn hóa về dải -1 đến 1 (PSI chuẩn)
    psi = weighted_sum / total
    return np.clip(psi, -1.0, 1.0)

def predict_trend(historical_psi):
    """
    Simple Moving Average to predict future trend direction.
    """
    if len(historical_psi) < 2:
        return "Stable"
    
    # Calculate simple trend direction
    diff = historical_psi[-1] - historical_psi[-2]
    if diff > 0.05:
        return "Positive Trend (Rising Approval)"
    elif diff < -0.05:
        return "Negative Trend (Rising Discontent)"
    else:
        return "Stable Trend"

def forecast_psi(historical_psi, days=3):
    """
    Dự báo PSI cho 'days' ngày tiếp theo bằng Linear Projection đơn giản.
    Dành cho phần "Dự đoán" của đề tài Transformer.
    """
    if len(historical_psi) < 3:
        return historical_psi # Không đủ dữ liệu để dự báo
    
    # Tính độ dốc trung bình của 3 điểm gần nhất
    slopes = [historical_psi[i] - historical_psi[i-1] for i in range(len(historical_psi)-1, len(historical_psi)-3, -1)]
    avg_slope = sum(slopes) / len(slopes)
    
    forecast = []
    last_val = historical_psi[-1]
    for _ in range(days):
        next_val = last_val + avg_slope
        # Giới hạn trong dải [-1, 1]
        next_val = np.clip(next_val, -1.0, 1.0)
        forecast.append(float(next_val))
        last_val = next_val
        
    return forecast

def generate_simulated_timeline(predictor, comments):
    """
    Simulate timeline by assigning fake timestamps to a batch of comments.
    """
    results = []
    base_time = datetime.now() - timedelta(days=7)
    
    for i, comment in enumerate(comments):
        pred = predictor.predict(comment)
        # Randomly distribute comments over 7 days for simulation
        timestamp = base_time + timedelta(hours=i * (168 / len(comments)))
        results.append({
            "timestamp": timestamp.isoformat(),
            "sentiment": pred["top_emotion"],
            "psi": calculate_psi(pred["probabilities"]),
            "text": comment
        })
    return results
