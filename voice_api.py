from flask import Flask, request, jsonify, send_file, after_this_request
import tempfile
import os
import requests

# Import chatbot logic from app.py
from app import initialize_chain

app = Flask(__name__)

# ElevenLabs API credentials (set these in your .env or environment)
ELEVEN_API_KEY = os.environ.get("ELEVEN_API_KEY", "your_elevenlabs_api_key")
ELEVEN_VOICE_ID = os.environ.get("ELEVEN_VOICE_ID", "your_voice_id")  # e.g. "21m00Tcm4TlvDq8ikWAM"
ELEVEN_STT_MODEL_ID = os.environ.get("ELEVEN_STT_MODEL_ID", "eleven_monolingual_v1")

# Initialize chatbot chain
chain = initialize_chain()

def transcribe_audio(audio_path):
    url = "https://api.elevenlabs.io/v1/speech-to-text"
    headers = {
        "xi-api-key": ELEVEN_API_KEY
    }
    data = {
        "model_id": "scribe_v1"
    }
    with open(audio_path, "rb") as f:
        files = {"file": f}
        response = requests.post(url, headers=headers, data=data, files=files)
    if response.status_code == 200:
        return response.json().get("text", "")
    else:
        raise Exception(f"STT Error: {response.text}")

def text_to_speech(text, output_path):
    url = f"https://api.elevenlabs.io/v1/text-to-speech/{ELEVEN_VOICE_ID}"
    headers = {
        "xi-api-key": ELEVEN_API_KEY,
        "Content-Type": "application/json"
    }
    data = {
        "text": text,
        "voice_settings": {
            "stability": 0.5,
            "similarity_boost": 0.5
        }
    }
    response = requests.post(url, headers=headers, json=data)
    if response.status_code == 200:
        with open(output_path, "wb") as f:
            f.write(response.content)
    else:
        raise Exception(f"TTS Error: {response.text}")

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
        tts_path = audio_path.replace(".wav", "_tts.mp3")
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
            mimetype="audio/mpeg",
            as_attachment=True,
            download_name="response.mp3"
        )
        response.headers["X-Transcript"] = user_text
        response.headers["X-Response"] = response_text
        return response
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001, debug=True) 