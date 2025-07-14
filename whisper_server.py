from flask import Flask, request, jsonify
import whisper
import tempfile
import os

app = Flask(__name__)
model = whisper.load_model("base")  # 모델: tiny, base, small, medium, large

@app.route('/transcribe', methods=['POST'])
def transcribe():
    try:
        if 'audio' not in request.files:
            return jsonify({'error': 'No audio file uploaded'}), 400

        audio_file = request.files['audio']
        
        if audio_file.filename == '':
            return jsonify({'error': 'No file selected'}), 400

        # 파일 확장자 추출
        filename = audio_file.filename
        file_extension = os.path.splitext(filename)[1] if filename else '.mp3'
        
        # 지원되는 확장자 목록
        supported_extensions = ['.mp3', '.wav', '.m4a', '.flac', '.ogg', '.wma']
        if file_extension.lower() not in supported_extensions:
            file_extension = '.mp3'  # 기본값

        # 임시 파일 생성 및 저장
        with tempfile.NamedTemporaryFile(delete=False, suffix=file_extension) as tmp:
            temp_file_path = tmp.name
            
        # 파일 핸들을 닫은 후 데이터 저장
        audio_file.save(temp_file_path)
        
        print(f"Processing audio file: {filename} -> {temp_file_path}")
        
        # 파일이 실제로 존재하는지 확인
        if not os.path.exists(temp_file_path):
            raise FileNotFoundError(f"Temporary file not found: {temp_file_path}")
            
        # 파일 크기 확인
        file_size = os.path.getsize(temp_file_path)
        print(f"Temporary file size: {file_size} bytes")
        
        if file_size == 0:
            raise ValueError("Uploaded file is empty")
            
        result = model.transcribe(temp_file_path)
        
        # 안전하게 임시 파일 삭제
        try:
            os.remove(temp_file_path)
        except OSError as e:
            print(f"Warning: Failed to delete temporary file {temp_file_path}: {e}")
            
        print(f"Transcription result: {result['text']}")

        return jsonify({'text': result["text"]})
    
    except Exception as e:
        print(f"Error during transcription: {str(e)}")
        return jsonify({'error': f'Transcription failed: {str(e)}'}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
