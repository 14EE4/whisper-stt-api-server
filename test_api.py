import requests
import json
import os
import glob

def test_transcribe_api():
    """
    Whisper STT API 테스트 함수
    audio_samples 폴더의 오디오 파일들을 자동으로 찾아서 테스트합니다.
    """
    url = "http://localhost:5000/transcribe"
    
    # 오디오 파일 폴더
    audio_folder = "audio_samples"
    
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
    
    # audio_samples 폴더 확인
    if not os.path.exists(audio_folder):
        print(f"✗ 오디오 폴더를 찾을 수 없습니다: {audio_folder}")
        print("  폴더를 생성하고 오디오 파일을 추가하세요.")
        return
    
    # 지원되는 오디오 파일 확장자
    audio_extensions = ['*.mp3', '*.wav', '*.m4a', '*.flac', '*.ogg', '*.wma']
    audio_files = []
    
    for ext in audio_extensions:
        audio_files.extend(glob.glob(os.path.join(audio_folder, ext)))
        audio_files.extend(glob.glob(os.path.join(audio_folder, ext.upper())))
    
    if not audio_files:
        print(f"✗ {audio_folder} 폴더에 오디오 파일이 없습니다.")
        print("  지원 형식: mp3, wav, m4a, flac, ogg, wma")
        return
    
    print(f"✓ {len(audio_files)}개의 오디오 파일을 발견했습니다:")
    for i, file_path in enumerate(audio_files, 1):
        filename = os.path.basename(file_path)
        file_size = os.path.getsize(file_path) / (1024 * 1024)  # MB
        print(f"  {i}. {filename} ({file_size:.2f} MB)")
    
    # 각 파일에 대해 테스트 수행
    for i, audio_file_path in enumerate(audio_files, 1):
        filename = os.path.basename(audio_file_path)
        print(f"\n[{i}/{len(audio_files)}] 테스트 중: {filename}")
        print("-" * 40)
        
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
    
    print(f"\n테스트 완료! 총 {len(audio_files)}개 파일 처리됨")
    print("\n새로운 오디오 파일 추가 방법:")
    print(f"1. {audio_folder} 폴더에 오디오 파일을 복사하세요")
    print("2. 이 스크립트를 다시 실행하면 자동으로 감지됩니다")

if __name__ == "__main__":
    test_transcribe_api()
