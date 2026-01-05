@echo off
chcp 65001 >nul
cd /d "%~dp0"

echo.
echo ====================================================
echo   Edge-TTS PRO - Text-to-Speech + Voice Cloning
echo ====================================================
echo.
echo   Đang khởi động giao diện web...
echo   Trình duyệt sẽ tự động mở trong vài giây
echo.
echo   Địa chỉ: http://localhost:8502
echo   Nhấn Ctrl+C để dừng
echo ====================================================
echo.

"D:/TOOOL DONGJ DDOC/.venv/Scripts/python.exe" -m streamlit run web_app_pro.py --server.port 8502
pause
