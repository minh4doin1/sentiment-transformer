import subprocess
import os
import sys
import time
import webbrowser

def run():
    print("🚀 Khởi chạy Sentiment AI Dashboard...")
    
    # 1. Kiểm tra xem model đã được train chưa
    model_path = "d:/side_project/sentiment-transformer-thesis/models/final_model"
    if not os.path.exists(model_path):
        print("⚠️ CẢNH BÁO: Không tìm thấy model tùy chỉnh (final_model).")
        print("💡 Vui lòng chạy Training trước nếu muốn dùng model của riêng bạn.")
        print("🔜 Hiện tại ứng dụng sẽ chạy ở chế độ Demo/Placeholder.")
    
    # 2. Chạy Backend
    print("📡 Đang khởi động Backend server (FastAPI)...")
    backend_process = subprocess.Popen(
        [sys.executable, "backend/app.py"],
        cwd="d:/side_project/sentiment-transformer-thesis"
    )
    
    # 3. Đợi server lên
    time.sleep(3)
    
    # 4. Mở Frontend trên trình duyệt
    frontend_path = os.path.abspath("frontend/index.html")
    print(f"🌐 Đang mở Dashboard tại: {frontend_path}")
    webbrowser.open(f"file:///{frontend_path}")
    
    print("\n✅ Hệ thống đã sẵn sàng!")
    print("⌨️ Nhấn Ctrl+C để dừng Backend.")
    
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\n🛑 Đang dừng Backend...")
        backend_process.terminate()
        print("👋 Tạm biệt!")

if __name__ == "__main__":
    run()
