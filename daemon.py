import threading
from wake import detect_wake_word
from main_logic import assistant_loop

def start_assistant():
    print("Jarvis Background Mode Started")

    threading.Thread(
        target=detect_wake_word,
        daemon=True
    ).start()

    assistant_loop()

if __name__ == "__main__":
    start_assistant()
