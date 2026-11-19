from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from datetime import datetime

db = SQLAlchemy()


# =========================
# USER MODEL
# =========================

class User(UserMixin, db.Model):

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    google_id = db.Column(
        db.String(200),
        unique=True,
        nullable=False
    )

    email = db.Column(
        db.String(200),
        unique=True,
        nullable=False
    )

    name = db.Column(
        db.String(200),
        nullable=False
    )

    # Daily message counter
    message_count = db.Column(
        db.Integer,
        default=0
    )

    # Date/time when message count was last reset
    last_reset = db.Column(
        db.DateTime,
        default=datetime.utcnow
    )


# =========================
# CHAT SESSION MODEL
# =========================

class ChatSession(db.Model):

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    user_id = db.Column(
        db.Integer,
        db.ForeignKey("user.id"),
        nullable=False,
        index=True
    )

    title = db.Column(
        db.String(200),
        nullable=False,
        default="New Chat"
    )

    created_at = db.Column(
        db.DateTime,
        default=datetime.utcnow
    )

    updated_at = db.Column(
        db.DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow
    )


# =========================
# CONVERSATION MODEL
# =========================

class Conversation(db.Model):

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    user_id = db.Column(
        db.Integer,
        db.ForeignKey("user.id"),
        nullable=False
    )

    chat_session_id = db.Column(
        db.Integer,
        db.ForeignKey("chat_session.id"),
        nullable=True,
        index=True
    )

    user_message = db.Column(
        db.Text,
        nullable=False
    )

    bot_response = db.Column(
        db.Text,
        nullable=False
    )

    created_at = db.Column(
        db.DateTime,
        default=datetime.utcnow
    )


# =========================
# INTEGRATION SETTINGS
# =========================

class Integration(db.Model):

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    user_id = db.Column(
    db.Integer,
    db.ForeignKey("user.id"),
    nullable=False
)
    

    # WhatsApp Integration
    whatsapp_number = db.Column(
        db.String(100)
    )

    whatsapp_phone_number_id = db.Column(
    db.String(100),
    nullable=True,
    unique=True
)

    whatsapp_api_key = db.Column(
        db.String(300)
    )

    # E-commerce Integration
    store_type = db.Column(
        db.String(100)
    )

    store_url = db.Column(
        db.String(300)
    )

    store_api_key = db.Column(
        db.String(300)
    )




# =========================
# WHATSAPP CONVERSATION MODEL
# =========================

class WhatsAppConversation(db.Model):

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    # Business owner of this conversation
    owner_user_id = db.Column(
        db.Integer,
        db.ForeignKey("user.id"),
        nullable=True,
        index=True
    )

    sender_id = db.Column(
        db.String(100),
        nullable=False,
        index=True
    )

    user_message = db.Column(
        db.Text,
        nullable=False
    )

    bot_response = db.Column(
        db.Text,
        nullable=False
    )

    created_at = db.Column(
        db.DateTime,
        default=datetime.utcnow
    )

# =========================
# PROCESSED WHATSAPP MESSAGES
# =========================

class WhatsAppProcessedMessage(db.Model):

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    # Meta's unique WhatsApp message ID
    message_id = db.Column(
        db.String(200),
        unique=True,
        nullable=False
    )

    created_at = db.Column(
        db.DateTime,
        default=datetime.utcnow
    )
