# Whisper STT API Server

OpenAI Whisper 모델을 사용한 음성 인식(Speech-to-Text) REST API 서버입니다.

## 📋 목차

- [시스템 요구사항](#시스템-요구사항)
- [설치 방법](#설치-방법)
- [서버 실행](#서버-실행)
- [API 사용법](#api-사용법)
- [테스트 방법](#테스트-방법)
- [지원 파일 형식](#지원-파일-형식)
- [문제 해결](#문제-해결)

## 🖥️ 시스템 요구사항

- **Python**: 3.10 이상
- **FFmpeg**: 오디오 파일 처리를 위해 필요
- **메모리**: 최소 4GB RAM (모델에 따라 다름)
- **운영체제**: Windows, macOS, Linux

## 🚀 설치 방법

### 1. Python 패키지 설치

```bash
pip install flask
pip install openai-whisper
pip install requests  # 테스트용
```

### 2. FFmpeg 설치 (Windows)

1. [FFmpeg 공식 사이트](https://ffmpeg.org/download.html)에서 Windows용 바이너리 다운로드
2. 압축 해제 후 적절한 위치에 설치 (예: `C:\ffmpeg`)
3. 환경변수 PATH에 FFmpeg bin 폴더 추가:
   - `시스템 속성` → `환경 변수` → `시스템 변수`의 `Path` 편집
   - `C:\ffmpeg\bin` 경로 추가
4. 새 명령 프롬프트/PowerShell에서 `ffmpeg -version` 실행하여 설치 확인

### 3. PATH 환경변수 새로고침 (재부팅 없이)

PowerShell에서:
```powershell
$env:Path = [System.Environment]::GetEnvironmentVariable("Path","Machine") + ";" + [System.Environment]::GetEnvironmentVariable("Path","User")
```

## 🏃‍♂️ 서버 실행

### 기본 실행
```bash
python whisper_server.py
```

서버가 시작되면 다음과 같은 메시지가 표시됩니다:
```
* Running on all addresses (0.0.0.0)
* Running on http://127.0.0.1:5000
* Running on http://[실제_IP_주소]:5000
```

### Whisper 모델 변경

`whisper_server.py` 파일에서 모델을 변경할 수 있습니다:

```python
# 사용 가능한 모델: tiny, base, small, medium, large
model = whisper.load_model("base")  # 원하는 모델로 변경
```

**모델별 특성:**
- `tiny`: 가장 빠름, 정확도 낮음 (~39MB)
- `base`: 균형잡힌 성능 (~74MB)
- `small`: 좋은 정확도 (~244MB)
- `medium`: 높은 정확도 (~769MB)
- `large`: 최고 정확도 (~1550MB)

## 📡 API 사용법

### 엔드포인트
```
POST http://localhost:5000/transcribe
```

### 요청 형식
- **Content-Type**: `multipart/form-data`
- **파라미터**: `audio` (파일)

### cURL 예제
```bash
curl -X POST -F "audio=@your_audio_file.mp3" http://localhost:5000/transcribe
```

### Python 예제
```python
import requests

url = "http://localhost:5000/transcribe"
with open("audio_file.mp3", "rb") as f:
    files = {"audio": f}
    response = requests.post(url, files=files)
    result = response.json()
    print(result["text"])
```

### 응답 형식

**성공 응답 (200):**
```json
{
    "text": "인식된 음성 텍스트가 여기에 표시됩니다."
}
```

**오류 응답 (400):**
```json
{
    "error": "No audio file uploaded"
}
```

**오류 응답 (500):**
```json
{
    "error": "Transcription failed: [오류 상세 내용]"
}
```

## 🧪 테스트 방법

### 자동 테스트 스크립트 사용

1. 테스트할 오디오 파일을 프로젝트 폴더에 복사
2. `test_api.py` 파일에서 파일 경로 수정:
   ```python
   audio_file_path = "your_audio_file.mp3"  # 실제 파일명으로 변경
   ```
3. 테스트 실행:
   ```bash
   python test_api.py
   ```

### 테스트 결과 예시
```
Whisper STT API 테스트
==================================================
서버 URL: http://localhost:5000/transcribe
✗ 서버에 연결되었지만 GET 요청은 지원하지 않습니다 (정상)
파일 없는 요청 테스트: 400
응답: {'error': 'No audio file uploaded'}

실제 오디오 파일 테스트:
==============================
✓ 오디오 파일 발견: 녹음 (7).m4a
음성 인식 중... (시간이 걸릴 수 있습니다)
✓ 상태 코드: 200
✓ 인식된 텍스트: 안녕하세요. 마이크 테스트 하나 둘 셋 하나 둘 셋
```

## 📁 지원 파일 형식

다음 오디오 형식을 지원합니다:
- MP3 (`.mp3`)
- WAV (`.wav`)
- M4A (`.m4a`)
- FLAC (`.flac`)
- OGG (`.ogg`)
- WMA (`.wma`)

## 🔧 문제 해결

### 1. "지정된 파일을 찾을 수 없습니다" 오류

**원인**: FFmpeg이 설치되지 않았거나 PATH에 등록되지 않음

**해결방법**:
1. FFmpeg 설치 확인: `ffmpeg -version`
2. PATH 환경변수에 FFmpeg 추가
3. PowerShell에서 PATH 새로고침:
   ```powershell
   $env:Path = [System.Environment]::GetEnvironmentVariable("Path","Machine") + ";" + [System.Environment]::GetEnvironmentVariable("Path","User")
   ```

### 2. 서버 연결 실패

**확인사항**:
- 서버가 실행 중인지 확인
- 포트 5000이 다른 프로그램에서 사용 중이지 않은지 확인
- 방화벽 설정 확인

### 3. 메모리 부족 오류

**해결방법**:
- 더 작은 모델 사용 (`tiny` 또는 `base`)
- 시스템 메모리 확인

### 4. 인식 정확도가 낮은 경우

**개선 방법**:
- 더 큰 모델 사용 (`medium` 또는 `large`)
- 오디오 품질 개선 (노이즈 제거, 명확한 발음)
- 적절한 볼륨으로 녹음

## 📝 프로젝트 구조

```
whisper-stt-api-server/
├── whisper_server.py      # 메인 서버 파일
├── test_api.py           # API 테스트 스크립트
├── README.md            # 이 파일
└── 녹음 (7).m4a         # 테스트용 오디오 파일 (예시)
```

## 🛡️ 보안 고려사항

- 이 서버는 개발/테스트용입니다
- 프로덕션 환경에서는 적절한 WSGI 서버 (gunicorn, uWSGI 등) 사용 권장
- 파일 업로드 크기 제한 고려
- 인증 및 권한 관리 추가 고려

## 📄 라이센스

이 프로젝트는 오픈소스이며, OpenAI Whisper 모델의 라이센스를 따릅니다.

## 🤝 기여하기

버그 리포트, 기능 제안, 풀 리퀘스트를 환영합니다!

---

**개발자**: 14ee4
**마지막 업데이트**: 2025년 7월 14일
