from stt import record_audio, transcribe
from brain import ask_ai
from tts import speak
from memory_db import init_db, save_memory

init_db()


def elite_loop():

    print("Elite Jarvis Activated")

    while True:

        record_audio(duration=3)

        text = transcribe()

        if not text:
            continue

        print("User:", text)

        response = ask_ai(text)

        save_memory(text, response)

        speak(response)
if __name__ == "__main__":
    elite_loop()