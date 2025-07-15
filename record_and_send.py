import sounddevice as sd
import numpy as np
import wave
import requests
import os
import tempfile
import sys
import platform

# Settings
SAMPLE_RATE = 16000  # Vosk model expects 16kHz
CHANNELS = 1
DURATION = 5  # seconds to record

print("Press Enter to start recording...")
input()
print(f"Recording for {DURATION} seconds. Speak now...")

recording = sd.rec(int(DURATION * SAMPLE_RATE), samplerate=SAMPLE_RATE, channels=CHANNELS, dtype='int16')
sd.wait()

# Save to temp WAV file
with tempfile.NamedTemporaryFile(suffix='.wav', delete=False) as tmp:
    wav_path = os.path.abspath(tmp.name)
    with wave.open(wav_path, 'wb') as wf:
        wf.setnchannels(CHANNELS)
        wf.setsampwidth(2)  # 16 bits = 2 bytes
        wf.setframerate(SAMPLE_RATE)
        wf.writeframes(recording.tobytes())

print(f"Audio recorded and saved to {wav_path}")

# Send to API
url = "http://127.0.0.1:5001/voice-assistant"
with open(wav_path, "rb") as f:
    files = {"audio": f}
    response = requests.post(url, files=files)

# Save and play bot response
if response.status_code == 200:
    with tempfile.NamedTemporaryFile(suffix='.wav', delete=False) as bot_tmp:
        bot_wav_path = os.path.abspath(bot_tmp.name)
        bot_tmp.write(response.content)
    print("Bot response audio saved as:", bot_wav_path)
    print("Transcript:", response.headers.get("X-Transcript"))
    print("Bot Response:", response.headers.get("X-Response"))
    print("Bot response absolute path:", bot_wav_path)
    # Playback (cross-platform)
    if platform.system() == "Darwin":
        os.system(f"afplay {bot_wav_path}")
    elif platform.system() == "Windows":
        import winsound
        winsound.PlaySound(bot_wav_path, winsound.SND_FILENAME)
    else:  # Linux
        os.system(f"aplay {bot_wav_path}")
else:
    print("Error:", response.text)

# Cleanup
os.remove(wav_path)
# Uncomment to auto-delete bot response audio after playback
# os.remove(bot_wav_path) 