from flask import Flask, request, jsonify, render_template, send_from_directory
import torch
import librosa
from transformers import Wav2Vec2Processor, Wav2Vec2ForCTC
from pydub import AudioSegment
import os

# Set up Flask app
app = Flask(__name__, static_folder='../web/assets', template_folder='../web')

# Load model and processor
model_path = "ASR_Deployment_Project/Model_weights"
model = Wav2Vec2ForCTC.from_pretrained(model_path)
processor = Wav2Vec2Processor.from_pretrained(model_path)

# Utility function to convert non-wav audio to wav
def convert_to_wav(file):
    if not file.filename.endswith('.wav'):
        audio = AudioSegment.from_file(file)
        wav_filename = f"{os.path.splitext(file.filename)[0]}.wav"
        wav_path = f"/tmp/{wav_filename}"  # Save in temporary directory
        audio.export(wav_path, format="wav")
        return wav_path
    else:
        return file

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/assets/<path:filename>')
def send_asset(filename):
    return send_from_directory(app.static_folder, filename)

@app.route('/transcribe', methods=['POST'])
def transcribe():
    try:
        if 'file' not in request.files:
            return jsonify({"error": "No file provided"}), 400

        file = request.files['file']
        if file:
            print("File received successfully")

        # Convert the file to wav if it is not a wav file
        file_path = convert_to_wav(file)
        
        # Load the audio file
        audio, _ = librosa.load(file_path, sr=16000)
        print("Audio loaded successfully")

        # Preprocess the audio for the model
        input_values = processor(audio, return_tensors="pt", sampling_rate=16000).input_values
        print("Audio preprocessed successfully")

        # Run the model inference
        with torch.no_grad():
            logits = model(input_values).logits
        print("Model inference completed")

        # Decode the logits to get transcription
        pred_ids = torch.argmax(logits, dim=-1)
        transcription = processor.decode(pred_ids[0])
        print(f"Transcription: {transcription}")

        # Clean up temporary files
        if file_path != file:
            os.remove(file_path)

        return jsonify({"transcription": transcription})
    except Exception as e:
        print(f"Error occurred: {e}")
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
