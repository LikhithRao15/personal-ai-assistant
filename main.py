from wake import detect_wake_word
from stt import record_audio, transcribe
from tts import speak
from commands import execute_command
from brain import ask_ai


def main():
    print("Assistant started.")

    while True:
        detect_wake_word()

        record_audio()
        text = transcribe()

        if text:
            response = execute_command(text)

            if response:
                speak(response)
            else:
                speak("I did not understand that command.")

if __name__ == "__main__":
    main()
