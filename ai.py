import requests
from config import Config


def generate_response(message):
    headers = {
        "Authorization": f"Bearer {Config.GPT_API_KEY}",
        "Content-Type": "application/json"
    }

    payload = {
        "model": "openai/gpt-oss-120b",
        "messages": [
            {
                "role": "system",
                "content": "You are a helpful AI assistant"
            },
            {
                "role": "user",
                "content": message
            }
        ],
        "temperature": 0.7,
        "max_tokens": 500
    }

    response = requests.post(
        Config.GPT_API_URL,
        headers=headers,
        json=payload
    )

    data = response.json()

    try:
        return data["choices"][0]["message"]["content"]
    except:
        return "Error generating AI response"