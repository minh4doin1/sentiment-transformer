# setup_environment.ps1
# Script chuẩn bị môi trường toàn diện cho dự án Sentiment AI (Vietnamese Sentiment Analysis)

$ErrorActionPreference = "Stop" # Dừng nếu có lỗi nghiêm trọng

Write-Host "================================================" -ForegroundColor Cyan
Write-Host "   SENTIMENT AI - CÀI ĐẶT MÔI TRƯỜNG TỰ ĐỘNG    " -ForegroundColor Cyan
Write-Host "================================================" -ForegroundColor Cyan

# 1. Kiểm tra Python
Write-Host "`n[1/6] Đang kiểm tra Python..." -ForegroundColor Yellow
$pythonPath = where.exe python 2>$null | Select-Object -First 1

if (-not $pythonPath) {
    Write-Host ">>> Không tìm thấy Python! Đang thử cài đặt qua winget..." -ForegroundColor Red
    try {
        winget install -e --id Python.Python.3.10 --silent --accept-package-agreements --accept-source-agreements
        Write-Host ">>> Đã cài đặt xong Python 3.10. Vui lòng khởi động lại Terminal và chạy lại script này." -ForegroundColor Green
        exit
    } catch {
        Write-Host ">>> LỖI: Không thể tự động cài đặt Python. Vui lòng tải tại: https://www.python.org/downloads/" -ForegroundColor Red
        exit 1
    }
}
Write-Host ">>> Đã tìm thấy Python: $pythonPath" -ForegroundColor Green

# 2. Tạo Virtual Environment (venv)
Write-Host "`n[2/6] Đang tạo môi trường ảo (venv)..." -ForegroundColor Yellow
if (-not (Test-Path "venv")) {
    python -m venv venv
    Write-Host ">>> Đã tạo venv thành công." -ForegroundColor Green
} else {
    Write-Host ">>> Venv đã tồn tại, bỏ qua bước này." -ForegroundColor Green
}

# 3. Nâng cấp pip và cài PyTorch (CPU)
Write-Host "`n[3/6] Đang cài đặt thư viện lõi (pip, torch)..." -ForegroundColor Yellow
& ".\venv\Scripts\python.exe" -m pip install --upgrade pip
& ".\venv\Scripts\pip.exe" install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cpu
Write-Host ">>> Hoàn tất cài đặt framework PyTorch." -ForegroundColor Green

# 4. Cài đặt các thư viện khác từ requirements.txt
Write-Host "`n[4/6] Đang cài đặt các dependencies khác..." -ForegroundColor Yellow
if (Test-Path "requirements.txt") {
    & ".\venv\Scripts\pip.exe" install -r requirements.txt
    Write-Host ">>> Đã cài đặt xong tất cả thư viện quan trọng." -ForegroundColor Green
} else {
    Write-Error ">>> LỖI: Không tìm thấy file requirements.txt!"
}

# 5. Tải dữ liệu mẫu (UIT-VSMEC)
Write-Host "`n[5/6] Đang khởi tạo dữ liệu mẫu..." -ForegroundColor Yellow
if (Test-Path "training/prepare_data.py") {
    & ".\venv\Scripts\python.exe" training/prepare_data.py
    Write-Host ">>> Dữ liệu đã sẵn sàng." -ForegroundColor Green
} else {
    Write-Host ">>> Cảnh báo: Không thấy script chuẩn bị dữ liệu, bỏ qua." -ForegroundColor Gray
}

# 6. Kiểm tra Model
Write-Host "`n[6/6] Kiểm tra Model weights..." -ForegroundColor Yellow
if (-not (Test-Path "models/final_model/config.json")) {
    Write-Host "--------------------------------------------------------" -ForegroundColor Red
    Write-Host " CHÚ Ý: CHƯA CÓ MODEL TRONG models/final_model/ " -ForegroundColor Red
    Write-Host " Bạn cần giải nén file 'final_model_pro.zip' (nếu có) "
    Write-Host " vào thư mục 'models/final_model/' trước khi chạy app."
    Write-Host "--------------------------------------------------------"
} else {
    Write-Host ">>> Model đã sẵn sàng." -ForegroundColor Green
}

# Tạo file shortcut chạy nhanh
@"
@echo off
echo Dang khoi dong Sentiment AI...
call venv\Scripts\activate
python backend/app.py
pause
"@ | Out-File -FilePath "chay_nhanh.bat" -Encoding utf8

Write-Host "`n================================================" -ForegroundColor Cyan
Write-Host "       CÀI ĐẶT HOÀN TẤT! CHÚC MỪNG BẠN!         " -ForegroundColor Cyan
Write-Host " Để chạy ứng dụng, hãy nhấp đúp vào: chay_nhanh.bat" -ForegroundColor Green
Write-Host "================================================" -ForegroundColor Cyan
