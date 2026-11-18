
import os
from dotenv import load_dotenv

load_dotenv()


class Config:

    SECRET_KEY = os.getenv("SECRET_KEY")

    SQLALCHEMY_DATABASE_URI = os.getenv(
        "DATABASE_URL",
        "sqlite:///chatagent.db"
    )

    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Groq API
    GPT_API_KEY = os.getenv("GROQ_API_KEY")

    GPT_API_URL = "https://api.groq.com/openai/v1/chat/completions"

    # Google OAuth
    GOOGLE_OAUTH_CLIENT_ID = os.getenv("GOOGLE_CLIENT_ID")

    GOOGLE_OAUTH_CLIENT_SECRET = os.getenv("GOOGLE_CLIENT_SECRET")
