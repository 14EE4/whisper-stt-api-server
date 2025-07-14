@echo off
echo Whisper STT API Server 설치 스크립트
echo =====================================

echo.
echo 1. Python 패키지 설치 중...
pip install -r requirements.txt

echo.
echo 2. FFmpeg 설치 확인...
ffmpeg -version >nul 2>&1
if %errorlevel% equ 0 (
    echo ✓ FFmpeg이 이미 설치되어 있습니다.
) else (
    echo ✗ FFmpeg이 설치되지 않았습니다.
    echo   FFmpeg을 설치하고 PATH에 추가해주세요.
    echo   자세한 내용은 README.md를 참고하세요.
)

echo.
echo 3. 설치 완료!
echo   서버 실행: python whisper_server.py
echo   테스트 실행: python test_api.py

pause
