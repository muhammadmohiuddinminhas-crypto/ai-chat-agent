from flask import Flask, render_template, request, jsonify, redirect, url_for
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from flask_dance.contrib.google import google
from datetime import datetime
import os

from config import Config
from database import db, User, Conversation, Integration
from auth import google_bp
from ai import generate_response


app = Flask(__name__)
app.config.from_object(Config)

# =========================
# DATABASE INIT
# =========================
db.init_app(app)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"

app.register_blueprint(google_bp, url_prefix="/login")


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


with app.app_context():
    db.create_all()


# =========================
# AUTH ROUTES
# =========================
@app.route("/")
def login():
    if current_user.is_authenticated:
        return redirect(url_for("chat"))
    return render_template("login.html")


@app.route("/google_login")
def google_login():
    if not google.authorized:
        return redirect(url_for("google.login"))

    resp = google.get("/oauth2/v2/userinfo")
    info = resp.json()

    google_id = info["id"]
    email = info["email"]
    name = info["name"]

    user = User.query.filter_by(google_id=google_id).first()

    if not user:
        user = User(
            google_id=google_id,
            email=email,
            name=name
        )
        db.session.add(user)
        db.session.commit()

    login_user(user)
    return redirect(url_for("chat"))


@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("login"))


# =========================
# CHAT PAGE
# =========================
@app.route("/chat")
@login_required
def chat():
    return render_template(
        "chat.html",
        user=current_user,
        limit=100   # FIX ADDED
    )

# =========================
# SETTINGS PAGE
# =========================
@app.route("/settings")
@login_required
def settings():
    integration = Integration.query.filter_by(user_id=current_user.id).first()

    return render_template(
        "settings.html",
        integration=integration
    )
# =========================
# AI API
# =========================
@app.route("/send", methods=["POST"])
@login_required
def send_message():
    data = request.get_json()
    user_message = data.get("message")

    ai_reply = generate_response(user_message)

    convo = Conversation(
        user_id=current_user.id,
        user_message=user_message,
        bot_response=ai_reply,
        timestamp=datetime.utcnow()
    )

    db.session.add(convo)
    db.session.commit()

    return jsonify({"reply": ai_reply})


# =========================
# RUN (FOR DEPLOYMENT)
# =========================
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)