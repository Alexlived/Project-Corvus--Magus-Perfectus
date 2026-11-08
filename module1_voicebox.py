import sounddevice as sd
import speech_recognition as sr
import pyttsx3
import numpy as np
import time

def speak(text):
    print(f"Corvus: {text}")

    engine = pyttsx3.init('sapi5')
    engine.setProperty('rate', 175)

    engine.say(text)
    engine.runAndWait()
    engine.stop()

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