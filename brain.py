import requests

def ask_ai(prompt):

    url = "http://localhost:11434/api/generate"

    data = {
        "model": "phi3",
        "prompt": prompt,
        "stream": False,
        "options": {
            "num_predict": 120,
            "temperature": 0.7
        }
    }

    response = requests.post(url, json=data)

    return response.json().get("response","")
