
import requests
from config import Config


def generate_response(message):

    if not Config.GPT_API_KEY:
        raise RuntimeError("Groq API key is not configured.")

    headers = {
        "Authorization": f"Bearer {Config.GPT_API_KEY}",
        "Content-Type": "application/json"
    }

    payload = {
        "model": "openai/gpt-oss-120b",

        "messages": [
            {
                "role": "system",
                "content": (
                    "You are a helpful AI assistant. "
                    "Provide clear, accurate and friendly answers."
                )
            },
            {
                "role": "user",
                "content": message
            }
        ],

        "temperature": 0.7,
        "max_completion_tokens": 500
    }

    try:

        response = requests.post(
            Config.GPT_API_URL,
            headers=headers,
            json=payload,
            timeout=45
        )

        response.raise_for_status()

        data = response.json()

        ai_reply = data["choices"][0]["message"]["content"]

        if not ai_reply:
            raise RuntimeError("The AI returned an empty response.")

        return ai_reply.strip()

    except requests.exceptions.Timeout:
        raise RuntimeError("Groq API request timed out.")

    except requests.exceptions.HTTPError as error:
        raise RuntimeError(
            f"Groq API returned HTTP {error.response.status_code}."
        )

    except requests.exceptions.RequestException:
        raise RuntimeError("Unable to connect to Groq API.")

    except (KeyError, IndexError, TypeError):
        raise RuntimeError("Unexpected response received from Groq API.")
