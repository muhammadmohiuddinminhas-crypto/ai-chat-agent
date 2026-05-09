from flask import Flask, render_template, request, jsonify, redirect, url_for
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from flask_dance.contrib.google import google
from datetime import datetime

from config import Config
from database import db, User, Conversation, Integration
from auth import google_bp
from ai import generate_response


app = Flask(__name__)
app.config.from_object(Config)


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


@app.route("/")
def login():
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

if __name__ == "__main__":
    print("🚀 Starting AI Chat Agent...")
    app.run(debug=True)