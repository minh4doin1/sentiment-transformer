# setup_and_run.ps1
# Automating Sentiment Analysis Project Setup

$ErrorActionPreference = "Continue" # Don't stop on minor errors

Write-Host "--- Start Sentiment AI Setup ---" -ForegroundColor Cyan

# 1. Find Python
Write-Host "--- Checking for Python ---" -ForegroundColor Yellow
$pythonPath = $null

# Check common installation directories
$commonPaths = @(
    "C:\Program Files\Python3*",
    "C:\Users\$env:USERNAME\AppData\Local\Programs\Python\Python3*",
    "D:\Python3*",
    "D:\Program Files\Python3*"
)

foreach ($path in $commonPaths) {
    if (Test-Path $path) {
        $found = Get-ChildItem -Path $path -Filter "python.exe" -Recurse -Depth 1 -ErrorAction SilentlyContinue | Select-Object -First 1
        if ($found) {
            $pythonPath = $found.FullName
            break
        }
    }
}

# Final fallback to PATH (even Store aliases)
if (-not $pythonPath) {
    $pythonPath = where.exe python 2>$null | Select-Object -First 1
}

if (-not $pythonPath) {
    Write-Error "Error: Python not found. Please install Python from python.org."
    exit 1
}

Write-Host "Using Python at: $pythonPath" -ForegroundColor Green
$binDir = Split-Path -Parent $pythonPath
$env:Path = "$binDir;$env:Path"

# 2. Virtual Environment
if (-not (Test-Path "venv")) {
    Write-Host "--- Creating venv ---" -ForegroundColor Yellow
    & "$pythonPath" -m venv venv
    Write-Host "Venv created." -ForegroundColor Green
} else {
    Write-Host "Venv already exists." -ForegroundColor Green
}

# 3. Install Dependencies
Write-Host "--- Installing Dependencies ---" -ForegroundColor Yellow
& ".\venv\Scripts\python.exe" -m pip install --upgrade pip
& ".\venv\Scripts\pip.exe" install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cpu
& ".\venv\Scripts\pip.exe" install -r requirements.txt
Write-Host "Dependencies installed." -ForegroundColor Green

# 4. Data Check
Write-Host "--- Preparing Data ---" -ForegroundColor Yellow
& ".\venv\Scripts\python.exe" training/prepare_data.py
Write-Host "Data ready." -ForegroundColor Green

# 5. Model Check
if (-not (Test-Path "models/final_model/config.json")) {
    Write-Host "--- WARNING: MODEL NOT FOUND ---" -ForegroundColor Red
    Write-Host "Ensure files from final_model_pro.zip are in models/final_model/"
}

# 6. Start Backend
Write-Host "--- Launching Backend ---" -ForegroundColor Green
Start-Process powershell -ArgumentList "-NoExit", "-Command", "& '.\venv\Scripts\python.exe' backend/app.py"

# 7. Launch Dashboard
$frontendPath = "$PSScriptRoot\frontend\index.html"
Write-Host "--- Opening Dashboard ---" -ForegroundColor Green
Start-Process "file:///$frontendPath"

Write-Host "--- SYSTEM READY ---" -ForegroundColor Cyan
