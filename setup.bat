@echo off
setlocal
echo ================================================
echo   BAT DAU CAI DAT SENTIMENT AI...
echo ================================================

:: Kiem tra quyen thuc thi PowerShell
powershell -ExecutionPolicy Bypass -File "setup_environment.ps1"

if %ERRORLEVEL% NEQ 0 (
    echo [LOI] Co loi xay ra trong qua trinh cai dat. Vui long kiem tra code.
) else (
    echo [HOAN TAT] Da cai dat xong!
)

pause
