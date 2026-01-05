@echo off
chcp 65001 >nul
cd /d "%~dp0"

echo.
echo ================================================
echo   DANH SACH GIONG NOI TIENG VIET
echo ================================================
echo.

"D:/TOOOL DONGJ DDOC/.venv/Scripts/python.exe" tts_cli.py --list-voices vi-VN

echo.
pause
