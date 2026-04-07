# 🎓 Khai thác cảm xúc & Dự báo xu hướng dư luận mạng xã hội (Vietnamese Sentiment Analysis)

Đề tài nghiên cứu sử dụng mô hình Transformer (PhoBERT) để phân tích 7 loại cảm xúc đặc thù trên mạng xã hội Việt Nam và tính toán chỉ số tâm trạng công chúng (PSI).

---

## 📁 Cấu trúc dự án
- `training/`: Mã nguồn huấn luyện (Fine-tuning) mô hình trên bộ dữ liệu UIT-VSMEC.
- `backend/`: API server xây dựng bằng FastAPI, xử lý logic phân tích và dự báo.
- `frontend/`: Dashboard giao diện người dùng hiện đại (HTML/CSS/JS).
- `models/`: Nơi lưu trữ trọng số mô hình (`final_model`).
- `data/`: Chứa các bộ dữ liệu CSV phục vụ huấn luyện.

---

## 🚀 Hướng dẫn cài đặt chi tiết

### 1. Cài đặt nhanh (Quick Setup - Khuyên dùng)
Nếu bạn đang dùng Windows, hãy chạy file **`setup.bat`** (Click đúp chuột). Script này sẽ tự động:
- Kiểm tra & Cài đặt Python (nếu thiếu).
- Tạo môi trường ảo `venv`.
- Cài đặt PyTorch và các thư viện cần thiết.
- Tải dữ liệu mẫu UIT-VSMEC.

Hoặc chạy lệnh sau trong PowerShell:
```powershell
.\setup.bat
```

### 2. Cài đặt thủ công (Manual Setup)
Nếu bạn muốn tự tay cấu hình:
```powershell
# Tạo môi trường ảo
python -m venv venv

# Kích hoạt môi trường (Windows)
.\venv\Scripts\activate
```

### 2. Cài đặt thư viện (Dependencies)
Tùy vào cấu hình máy của bạn, hãy chọn **MỘT TRONG HAI** cách cài đặt sau:

#### A. Đối với máy huấn luyện bằng CPU (Ví dụ: i7-1355U)
Cách này nhẹ (chỉ ~200MB) và tốc độ tải nhanh hơn:
```powershell
pip install torch torchvision torchaudio --force-reinstall
pip install -r requirements.txt
```

#### B. Đối với máy có GPU NVIDIA (Cần CUDA)
Dành cho việc huấn luyện cực nhanh (15-30 phút):
```powershell
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118
pip install -r requirements.txt
```

---

## 📊 Quy trình Huấn luyện (Training)

Nếu bạn clone dự án này về máy mới (như máy i7), bạn cần huấn luyện lại mô hình từ đầu vì file trọng số (540MB) đã được loại bỏ để rút gọn dung lượng Git.

1. **Chuẩn bị dữ liệu**:
   ```powershell
   python training/prepare_data.py
   ```
2. **Bắt đầu huấn luyện**:
   ```powershell
   python training/train_model.py
   ```
   - **Lưu ý**: Trên CPU i7 đời 13, quá trình này mất khoảng **45-60 phút**. Kết quả cuối cùng sẽ được lưu tại `models/final_model`.

---

## 💻 Khởi chạy ứng dụng (Running)

Sau khi đã có model trong thư mục `models/final_model`, hãy thực hiện các bước sau:

1. **Chạy Backend API**:
   ```powershell
   python backend/app.py
   ```
   *Server sẽ lắng nghe tại cổng `8000`.*

2. **Mở Dashboard**:
   - Mở file `frontend/index.html` bằng trình duyệt (hoặc dùng Live Server trong VS Code).
   - Nhập một câu tiếng Việt và nhấn **"Phân tích"** để xem kết quả.

---

## 🧪 Giải thích Chỉ số PSI
Hệ thống sử dụng chỉ số **Public Sentiment Index (PSI)** để đo lường độ tích cực/tiêu cực của dư luận trong dải từ **[-1, 1]**:
- **PSI > 0**: Dư luận đang tích cực (Vui vẻ, Ngạc nhiên).
- **PSI < 0**: Dư luận đang có dấu hiệu tiêu cực (Phẫn nộ, Chán ghét, Sợ hãi).

Hệ thống cũng tự động **Highlight** các từ khóa cảm xúc dựa trên bộ từ điển (Lexicon) để giải thích lý do tại sao AI đưa ra kết quả đó.

---

