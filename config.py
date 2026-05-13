import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    SECRET_KEY = os.getenv("SECRET_KEY", "supersecretkey")

    SQLALCHEMY_DATABASE_URI = "sqlite:///chatagent.db"
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    GPT_API_KEY = os.getenv("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")
    GPT_API_URL = "https://api.groq.com/openai/v1/chat/completions"

    GOOGLE_OAUTH_CLIENT_ID = os.getenv("865453545088-rh4i9e3mi5lu31jg74061f3gtf20gj0r.apps.googleusercontent.com")
    GOOGLE_OAUTH_CLIENT_SECRET = os.getenv("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")

