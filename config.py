import os

class Config:
    SECRET_KEY = os.getenv("SECRET_KEY", "supersecretkey")

    SQLALCHEMY_DATABASE_URI = "sqlite:///chatagent.db"
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # GPT API
    GPT_API_KEY = os.getenv("GPT_API_KEY")
    GPT_API_URL = "https://api.groq.com/openai/v1/chat/completions"

    # Google OAuth
    GOOGLE_OAUTH_CLIENT_ID = os.getenv("GOOGLE_CLIENT_ID")
    GOOGLE_OAUTH_CLIENT_SECRET = os.getenv("GOOGLE_CLIENT_SECRET")

    DAILY_FREE_LIMIT = 100