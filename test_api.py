import requests
import json

def test_transcribe_api():
    """
    Whisper STT API 테스트 함수
    실제 오디오 파일을 업로드하여 테스트하려면 파일 경로를 수정하세요.
    """
    url = "http://localhost:5000/transcribe"
    
    # 테스트용 오디오 파일 경로
    audio_file_path = "녹음 (7).m4a"  # 폴더에 있는 실제 오디오 파일
    
    print("Whisper STT API 테스트")
    print("="*50)
    print(f"서버 URL: {url}")
    
    # 서버 연결 테스트
    try:
        response = requests.get("http://localhost:5000/")
        print("✗ 서버에 연결되었지만 GET 요청은 지원하지 않습니다 (정상)")
    except requests.exceptions.ConnectionError:
        print("✗ 서버에 연결할 수 없습니다. 서버가 실행 중인지 확인하세요.")
        return
    
    # 파일 없이 POST 요청 테스트 (에러 응답 확인)
    try:
        response = requests.post(url)
        print(f"파일 없는 요청 테스트: {response.status_code}")
        print(f"응답: {response.json()}")
    except Exception as e:
        print(f"요청 실패: {e}")
    
    print("\n실제 오디오 파일 테스트:")
    print("="*30)
    
    # 오디오 파일이 존재하는지 확인
    import os
    if not os.path.exists(audio_file_path):
        print(f"✗ 오디오 파일을 찾을 수 없습니다: {audio_file_path}")
        return
    
    print(f"✓ 오디오 파일 발견: {audio_file_path}")
    
    # 실제 오디오 파일로 테스트
    try:
        with open(audio_file_path, 'rb') as f:
            files = {'audio': f}
            print("음성 인식 중... (시간이 걸릴 수 있습니다)")
            response = requests.post(url, files=files)
            print(f"✓ 상태 코드: {response.status_code}")
            if response.status_code == 200:
                result = response.json()
                print(f"✓ 인식된 텍스트: {result['text']}")
            else:
                print(f"✗ 오류 응답:")
                print(f"   응답 텍스트: {response.text}")
                try:
                    error_json = response.json()
                    print(f"   JSON 오류: {error_json}")
                except:
                    print(f"   JSON 파싱 실패")
    except Exception as e:
        print(f"✗ 파일 업로드 실패: {e}")
    
    print("\n추가 테스트를 위해 다른 오디오 파일을 사용하려면:")
    print("1. 오디오 파일을 이 폴더에 복사하세요")
    print("2. audio_file_path 변수를 수정하세요")

if __name__ == "__main__":
    test_transcribe_api()
