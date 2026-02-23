from stt import record_audio, transcribe
from brain import ask_ai
from tts import speak

def assistant_loop():

    while True:

        print("Waiting for wake word...")

        # Wake word detected → code jumps here

        record_audio()

        text = transcribe()

        if text:
            print("User:", text)

            response = ask_ai(text)

            speak(response)
