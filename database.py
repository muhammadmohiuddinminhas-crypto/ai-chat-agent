from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from datetime import datetime


db = SQLAlchemy()


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    google_id = db.Column(db.String(200), unique=True)
    email = db.Column(db.String(200), unique=True)
    name = db.Column(db.String(200))
    message_count = db.Column(db.Integer, default=0)
    last_reset = db.Column(db.DateTime, default=datetime.utcnow)


class Conversation(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer)
    user_message = db.Column(db.Text)
    bot_reply = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)


class Integration(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer)

    whatsapp_number = db.Column(db.String(100))
    whatsapp_api_key = db.Column(db.String(300))

    store_type = db.Column(db.String(100))
    store_url = db.Column(db.String(300))
    store_api_key = db.Column(db.String(300))