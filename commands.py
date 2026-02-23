import os
import datetime

def execute_command(text):

    text = text.lower()

    # Open Chrome
    if "open chrome" in text:
        os.system("open -a 'Google Chrome'")
        return "Opening Chrome"

    # Open VS Code
    elif "open code" in text or "open vs code" in text:
        os.system("open -a 'Visual Studio Code'")
        return "Opening Visual Studio Code"

    # Time
    elif "time" in text:
        now = datetime.datetime.now().strftime("%I:%M %p")
        return f"The time is {now}"

    # Create folder
    elif "create folder" in text:
        words = text.split("create folder")
        if len(words) > 1:
            folder_name = words[1].strip()
            if folder_name:
                os.makedirs(folder_name, exist_ok=True)
                return f"Folder {folder_name} created"
        return "Please tell me the folder name"

    # Shutdown (safe version)
    elif "shut down" in text:
        return "Shutdown command detected. Confirmation required."

    else:
        return None
