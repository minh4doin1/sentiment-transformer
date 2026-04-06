# 🎓 Hướng dẫn Đề tài: Khai thác cảm xúc & Dự báo xu hướng dư luận mạng xã hội

Đề tài này tập trung vào việc sử dụng mô hình **Transformer (PhoBERT)** để phân tích 7 loại cảm xúc từ văn bản tiếng Việt và dự báo xu hướng dư luận xã hội thông qua chỉ số PSI.

## 📁 Cấu trúc thư mục
- `training/`: Chứa mã nguồn huấn luyện mô hình trên bộ dữ liệu UIT-VSMEC.
- `backend/`: API server xây dựng bằng FastAPI, xử lý logic phân tích và dự báo.
- `frontend/`: Dashboard giao diện người dùng (HTML/CSS/JS).
- `models/`: Nơi lưu trữ trọng số mô hình sau khi huấn luyện.

## 🚀 Quy trình thực hiện

### 1. Chuẩn bị dữ liệu
Chạy script để tải bộ dữ liệu UIT-VSMEC từ HuggingFace:
```bash
venv\Scripts\python training\prepare_data.py
```

### 2. Huấn luyện mô hình (Fine-tuning)
Mô hình sử dụng kiến trúc **PhoBERT-base**. Quá trình huấn luyện sẽ tối ưu hóa các trọng số cho bài toán phân loại 7 cảm xúc:
```bash
venv\Scripts\python training\train_model.py
```
*Lưu ý: Nếu có GPU NVIDIA, quá trình này sẽ mất khoảng 15-30 phút. Nếu dùng CPU sẽ mất vài tiếng.*

### 3. Chạy ứng dụng
Sau khi đã có model trong thư mục `models/final_model`, khởi chạy Backend:
```bash
venv\Scripts\python backend/app.py
```
Và mở file `frontend/index.html` trên trình duyệt để sử dụng Dashboard.

## 📊 Phương pháp nghiên cứu

### Mô hình Transformer
Hệ thống sử dụng **PhoBERT** (Pre-trained RoBERTa cho tiếng Việt). Quá trình **Fine-tuning** giúp mô hình thích nghi với ngôn ngữ mạng xã hội (Teencode, từ lóng) và các nhãn cảm xúc cụ thể.

### Chỉ số Tâm trạng Công chúng (PSI)
Chỉ số PSI (Public Sentiment Index) được tính toán theo công thức:
`PSI = (Positive - Negative) / Total`
- **Positive**: Cảm xúc Vui vẻ (Enjoyment).
- **Negative**: Buồn bã, Phẫn nộ, Sợ hãi, Chán ghét.
- Giá trị PSI nằm trong khoảng `[-1, 1]`. PSI > 0 thể hiện dư luận đang tích cực.

## 🛠️ Xử lý Teencode & Sai chính tả
Hệ thống được tích hợp bộ lọc chuẩn hóa (`backend/core/normalizer.py`) giúp xử lý các trường hợp viết tắt phổ biến như `ko`, `dc`, `j`,... giúp tăng độ chính xác khi phân tích dữ liệu thực tế trên MXH.
