import sounddevice as sd
import numpy as np
import soundfile as sf
import requests
import os
import tempfile
import sys
import platform

# Settings
SAMPLE_RATE = 16000  # ElevenLabs STT expects 16kHz mono WAV
CHANNELS = 1
DURATION = 5  # seconds to record

print("Press Enter to start recording (for ElevenLabs-powered voice assistant)...")
input()
print(f"Recording for {DURATION} seconds. Speak now...")

recording = sd.rec(int(DURATION * SAMPLE_RATE), samplerate=SAMPLE_RATE, channels=CHANNELS, dtype='int16')
sd.wait()

# Save to temp WAV file using soundfile for standard PCM_16
with tempfile.NamedTemporaryFile(suffix='.wav', delete=False) as tmp:
    wav_path = os.path.abspath(tmp.name)
    sf.write(wav_path, recording, SAMPLE_RATE, subtype='PCM_16')

print(f"Audio recorded and saved to {wav_path}")

# Send to API
url = "http://127.0.0.1:5001/voice-assistant"
with open(wav_path, "rb") as f:
    files = {"audio": f}
    response = requests.post(url, files=files)

# Save and play bot response
if response.status_code == 200:
    with tempfile.NamedTemporaryFile(suffix='.mp3', delete=False) as bot_tmp:
        bot_mp3_path = os.path.abspath(bot_tmp.name)
        bot_tmp.write(response.content)
    print("Bot response audio saved as:", bot_mp3_path)
    print("Transcript:", response.headers.get("X-Transcript"))
    print("Bot Response:", response.headers.get("X-Response"))
    print("Bot response absolute path:", bot_mp3_path)
    # Playback (cross-platform, for mp3)
    ext = os.path.splitext(bot_mp3_path)[1].lower()
    if platform.system() == "Darwin":
        os.system(f"afplay {bot_mp3_path}")
    elif platform.system() == "Windows":
        import winsound
        winsound.PlaySound(bot_mp3_path, winsound.SND_FILENAME)
    else:  # Linux
        import subprocess
        if ext == ".mp3":
            if subprocess.call(["which", "ffplay"], stdout=subprocess.DEVNULL) == 0:
                os.system(f"ffplay -autoexit -nodisp {bot_mp3_path}")
            elif subprocess.call(["which", "vlc"], stdout=subprocess.DEVNULL) == 0:
                os.system(f"cvlc --play-and-exit {bot_mp3_path}")
            else:
                print("No suitable MP3 player found (install ffmpeg or vlc). Cannot play MP3 on Linux with aplay.")
        else:
            os.system(f"aplay {bot_mp3_path}")
else:
    print("Error:", response.text)

# Cleanup
os.remove(wav_path)
# Uncomment to auto-delete bot response audio after playback
# os.remove(bot_wav_path) 