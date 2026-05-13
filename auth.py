from flask_dance.contrib.google import make_google_blueprint
from config import Config


google_bp = make_google_blueprint(
    client_id=Config.GOOGLE_OAUTH_CLIENT_ID,
    client_secret=Config.GOOGLE_OAUTH_CLIENT_SECRET,
    scope=[
        "openid",
        "https://www.googleapis.com/auth/userinfo.email",
        "https://www.googleapis.com/auth/userinfo.profile"
    ],
    redirect_url="/google_login"
)