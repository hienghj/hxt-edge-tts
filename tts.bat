@echo off
chcp 65001 >nul
cd /d "%~dp0"

if "%~1"=="" (
    echo.
    echo ========================================
    echo   EDGE-TTS - Chuyen van ban thanh giong noi
    echo ========================================
    echo.
    echo Su dung:
    echo   tts.bat "Van ban cua ban" [ten_file.mp3] [giong]
    echo.
    echo Vi du:
    echo   tts.bat "Xin chao" hello.mp3
    echo   tts.bat "Xin chao" hello.mp3 vi-VN-NamMinhNeural
    echo   tts.bat "Xin chao"
    echo.
    pause
    exit /b
)

set TEXT=%~1
set OUTPUT=%~2
set VOICE=%~3

if "%OUTPUT%"=="" (
    for /f "tokens=2-4 delims=/ " %%a in ('date /t') do (set mydate=%%c%%b%%a)
    for /f "tokens=1-2 delims=/:" %%a in ('time /t') do (set mytime=%%a%%b)
    set OUTPUT=output_%mydate%_%mytime%.mp3
)

if "%VOICE%"=="" (
    "D:/TOOOL DONGJ DDOC/.venv/Scripts/python.exe" tts_cli.py -t "%TEXT%" -o "%OUTPUT%"
) else (
    "D:/TOOOL DONGJ DDOC/.venv/Scripts/python.exe" tts_cli.py -t "%TEXT%" -o "%OUTPUT%" -v "%VOICE%"
)

if exist "%OUTPUT%" (
    echo.
    echo ======================================
    echo   Thanh cong! File da duoc tao:
    echo   %OUTPUT%
    echo ======================================
    echo.
)

pause
