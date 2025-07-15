from flask import Flask, request, jsonify, send_file, after_this_request
import tempfile
import os
import wave
import json as jsonlib
import pyttsx3
from vosk import Model, KaldiRecognizer
import numpy as np
import time

# Import chatbot logic from app.py
from app import initialize_chain

app = Flask(__name__)

# Load Vosk model (download and extract a model, e.g. vosk-model-small-en-us-0.15)
VOSK_MODEL_PATH = os.environ.get("VOSK_MODEL_PATH", "vosk-model-en-us-0.22")
vosk_model = Model(VOSK_MODEL_PATH)

# Initialize chatbot chain
chain = initialize_chain()

def transcribe_audio(audio_path):
    wf = wave.open(audio_path, "rb")
    rec = KaldiRecognizer(vosk_model, wf.getframerate())
    rec.SetWords(True)
    results = []
    while True:
        data = wf.readframes(4000)
        if len(data) == 0:
            break
        if rec.AcceptWaveform(data):
            results.append(jsonlib.loads(rec.Result()))
    results.append(jsonlib.loads(rec.FinalResult()))
    text = " ".join([r.get("text", "") for r in results])
    return text.strip()

def text_to_speech(text, output_path):
    engine = pyttsx3.init()
    engine.save_to_file(text, output_path)
    engine.runAndWait()
    # Wait for file to be written (pyttsx3 bug workaround)
    timeout = 5  # seconds
    poll_interval = 0.05
    waited = 0
    while not os.path.exists(output_path) and waited < timeout:
        time.sleep(poll_interval)
        waited += poll_interval
    # Also check file size is nonzero
    waited2 = 0
    while os.path.exists(output_path) and os.path.getsize(output_path) == 0 and waited2 < timeout:
        time.sleep(poll_interval)
        waited2 += poll_interval

@app.route("/voice-assistant", methods=["POST"])
def voice_assistant():
    if "audio" not in request.files:
        return jsonify({"error": "No audio file provided."}), 400
    audio_file = request.files["audio"]
    with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as tmp:
        audio_path = tmp.name
        audio_file.save(audio_path)
    try:
        # Transcribe
        user_text = transcribe_audio(audio_path)
        if not user_text:
            return jsonify({"error": "Could not transcribe audio."}), 400
        # Get chatbot response
        result = chain.invoke({"question": user_text})
        response_text = result["answer"]
        # TTS
        tts_path = audio_path.replace(".wav", "_tts.wav")
        text_to_speech(response_text, tts_path)
        # Schedule cleanup after response is sent
        @after_this_request
        def cleanup(response):
            try:
                os.remove(audio_path)
            except Exception:
                pass
            try:
                os.remove(tts_path)
            except Exception:
                pass
            return response
        # Return both text and audio
        response = send_file(
            tts_path,
            mimetype="audio/wav",
            as_attachment=True,
            download_name="response.wav"
        )
        response.headers["X-Transcript"] = user_text
        response.headers["X-Response"] = response_text
        return response
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001, debug=True) 