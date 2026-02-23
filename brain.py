import requests

def ask_ai(prompt):
    url = "http://localhost:11434/api/generate"

    data = {
        "model": "llama3",
        "prompt": prompt,
        "stream": False
    }

    response = requests.post(url, json=data)
    result = response.json()

    return result["response"]
