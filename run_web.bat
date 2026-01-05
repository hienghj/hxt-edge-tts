@echo off
chcp 65001 >nul
cd /d "%~dp0"

echo.
echo ====================================================
echo   Đang khởi động Edge-TTS Web Interface...
echo ====================================================
echo.
echo   Trình duyệt sẽ tự động mở trong vài giây
echo   Nếu không mở, hãy truy cập: http://localhost:8501
echo.
echo   Nhấn Ctrl+C để dừng server
echo ====================================================
echo.

"D:/TOOOL DONGJ DDOC/.venv/Scripts/python.exe" -m streamlit run web_app.py
pause
