# 📝 Báo cáo Tổng thể Hệ thống: Phân tích Cảm xúc Dư luận Mạng xã hội (Vietnamese Sentiment AI)

Dài tài nghiên cứu này tập trung vào việc xây dựng một hệ thống AI hoàn chỉnh từ khâu thu thập dữ liệu, huấn luyện mô hình học sâu cho đến triển khai giao diện người dùng (Dashboard) để theo dõi tâm trạng công chúng.

---

## 1. Mục tiêu và Kiến trúc Tổng quan

Hệ thống được thiết kế để giải quyết bài toán: **"Làm sao để máy tính hiểu được sắc thái tình cảm phức tạp trong tiếng Việt của người dùng mạng xã hội?"**

### Thành phần chính:
- **Lớp Dữ liệu**: Sử dụng bộ dữ liệu chuẩn UIT-VSMEC với 7 nhãn cảm xúc.
- **Lớp Mô hình (Brain)**: Dựa trên kiến trúc Transformer (PhoBERT-base) được tinh chỉnh (Fine-tuning).
- **Lớp API (Bridge)**: Xây dựng bằng FastAPI để cung cấp dịch vụ phân tích thời gian thực.
- **Lớp Dashboard (Visual)**: Giao diện web hiện đại giúp trực quan hóa kết quả và dự báo xu hướng.

---

## 2. Quá trình Xử lý Dữ liệu

### 📋 Bộ dữ liệu UIT-VSMEC
- Gồm hàng ngàn câu bình luận từ Facebook và các trang mạng xã hội.
- **7 loại cảm xúc**: Enjoyment (Vui vẻ), Sadness (Buồn), Fear (Sợ hãi), Anger (Phẫn nộ), Disgust (Chán ghét), Surprise (Ngạc nhiên) và Other (Khác).

### 🛠️ Tiền xử lý (Preprocessing)
1. **Chuẩn hóa Teencode**: Chuyển các từ viết tắt, từ lóng (vd: "hp" -> "hạnh phúc", "k" -> "không") về dạng chuẩn bằng bộ từ điển tùy chỉnh.
2. **Tách từ (Word Segmentation)**: Sử dụng thư viện `underthesea` để tách từ tiếng Việt theo đúng ngữ pháp (vd: "học sinh" thay vì "học" "sinh").
3. **Lexicon Extraction**: Trích xuất các từ khóa mang tính cảm xúc mạnh để hỗ trợ việc giải thích kết quả AI (Explainable AI).

---

## 3. Huấn luyện Mô hình (Training Phase)

### 🧠 Chiến lược Huấn luyện
Dữ liệu mạng xã hội thường bị **mất cân bằng** (ví dụ: số câu "Vui vẻ" nhiều hơn rất nhiều so với "Sợ hãi"). 

**Giải pháp**: Sử dụng **Weighted Cross Entropy Loss**.
- Hệ thống tự động tính toán trọng số theo tần suất xuất hiện của nhãn.
- Nhãn hiếm (như Surprise có trọng số x24) sẽ được mô hình "chăm sóc" kỹ hơn để tránh bị bỏ sót.

### ⚙️ Thông số kỹ thuật (Hyperparameters)
- **Base Model**: `vinai/phobert-base` (Pre-trained trên 20GB dữ liệu tiếng Việt).
- **Learning Rate**: `2e-5` (Tốc độ học nhỏ để không làm hỏng các kiến thức đã có của mô hình).
- **Batch Size**: 8 (Tối ưu cho bộ nhớ GPU 6GB-8GB).
- **Epochs**: 3 vòng huấn luyện toàn bộ dữ liệu.
- **Optimizer**: AdamW với Weight Decay `0.01` nhằm chống quá tải (Overfitting).

---

## 4. Xây dựng Hệ thống Backend & Frontend

### ⚡ Backend (FastAPI)
- **High Precision**: Thiết lập ngưỡng tin cậy (Threshold) 0.5. Nếu mô hình không chắc chắn > 50%, nó sẽ trả về kết quả "Uncertain" thay vì đoán sai.
- **PSI Calculation**: Công toán chỉ số tâm trạng công chúng (Public Sentiment Index) dựa trên trọng số các cảm xúc tích cực vs tiêu cực.
- **Simulated Analytics**: Thuật toán dự báo xu hướng (Trend prediction) dựa trên dữ liệu lịch sử để đưa ra cảnh báo sớm về khủng hoảng truyền thông.

### 🎨 Frontend (Dashboard)
- **Aesthetics**: Thiết kế theo phong cách Glassmorphism (Kính mờ) hiện đại.
- **Charts**: Sử dụng Chart.js để vẽ biểu đồ tròn (phân bổ cảm xúc) và biểu đồ đường (biến thiên chỉ số PSI).
- **Micro-interactions**: Các hiệu ứng hover và animation mượt mà khi trả về kết quả phân tích.

---

## 5. Kết luận & Hướng phát triển

Hệ thống đã đạt được sự cân bằng giữa **độ chính xác của AI** và **trải nghiệm người dùng**. 

### Kết quả đạt được:
- Nhận diện tốt các sắc thái cảm xúc đặc thù của người Việt.
- Giải quyết được vấn đề dữ liệu lệch (Imbalanced problem).
- Dashboard cung cấp cái nhìn trực quan, dễ hiểu cho người quản lý.

### Hướng phát triển:
1. Tích hợp thêm phân tích cảm xúc qua giọng nói (Speech-to-Sentiment).
2. Mở rộng bộ từ điển Teencode để cập nhật các thuật ngữ mới của Gen Z.
3. Triển khai mô hình lên các nền tảng đám mây (Azure/AWS) để phục vụ quy mô lớn.

---
*Báo cáo được tổng hợp tự động bởi Antigravity AI Assistant.*
