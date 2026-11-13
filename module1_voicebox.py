import sounddevice as sd
import speech_recognition as sr
import pyttsx3
import numpy as np
import time
import wave
from piper.voice import PiperVoice

MODEL_PATH = "en_GB-northern_english_male-medium.onnx"
voice = PiperVoice.load(MODEL_PATH)


def speak(text):
    if not text:
        return
    print(f"[Corvus]: {text}")

    with sd.RawOutputStream(
        samplerate=voice.config.sample_rate,
        channels=1,
        dtype="int16"
    ) as stream:
        for chunk in voice.synthesize(text):
            stream.write(chunk.audio_int16_bytes)


def listen_and_recognize(duration=5,fs=16000,  silence_limit=1.2, threshold=1500):
    print("\n[Status] Listening...")

    audio_chunks = []

    speaking = False
    silence_start = None

    with sd.InputStream(
        samplerate=fs,
        channels=1,
        dtype="int16",
        blocksize=1024
    ) as stream:

        while True:

            audio, overflowed = stream.read(1024)

            volume = np.abs(audio).mean()
            if volume > threshold:

                speaking = True
                silence_start = None

            elif speaking:

                if silence_start is None:
                    silence_start = time.time()

                elif time.time() - silence_start >= silence_limit:
                    break

            if speaking:
                audio_chunks.append(audio.copy())

    print("[Status] Processing speech...")


    recorded_audio = np.concatenate(audio_chunks)

    recognizer = sr.Recognizer()

    audio_data = sr.AudioData(
        recorded_audio.tobytes(),
        sample_rate=fs,
        sample_width=2
    )

    try:
        text = recognizer.recognize_google(audio_data)

        print(f"You said: {text}")

        return text.lower()

    except sr.UnknownValueError:
        print("Could not understand audio.")
        return ""

    except sr.RequestError as e:
        print(f"Google recognition error: {e}")
        return ""


if __name__ == "__main__":

    speak("Voice box online, sir.")
    
    user_speech = listen_and_recognize()
    if user_speech:
        speak(f"I heard you say: {user_speech}")