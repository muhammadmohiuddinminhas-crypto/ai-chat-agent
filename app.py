import os
import requests
from sqlalchemy.exc import IntegrityError

from flask import (
    Flask,
    render_template,
    request,
    jsonify,
    redirect,
    url_for
)

from flask_login import (
    LoginManager,
    login_user,
    logout_user,
    login_required,
    current_user
)

from flask_dance.contrib.google import google

from datetime import datetime, date
import os

from config import Config
from database import (
    db,
    User,
    ChatSession,
    Conversation,
    Integration,
    WhatsAppConversation,
    WhatsAppProcessedMessage
)
from auth import google_bp
from ai import generate_response


# ==========================================
# APPLICATION CONFIGURATION
# ==========================================

app = Flask(__name__)
app.config.from_object(Config)

from werkzeug.middleware.proxy_fix import ProxyFix

app.wsgi_app = ProxyFix(
    app.wsgi_app,
    x_proto=1,
    x_host=1
)

# Allow HTTP for local OAuth development only
os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"

# ==========================================
# REGISTER GOOGLE LOGIN (ONLY ONCE)
# ==========================================

app.register_blueprint(
    google_bp,
    url_prefix="/login"
)


# ==========================================
# DATABASE INITIALIZATION
# ==========================================

db.init_app(app)

with app.app_context():
    db.create_all()


# ==========================================
# LOGIN MANAGER
# ==========================================

login_manager = LoginManager()

login_manager.init_app(app)

login_manager.login_view = "login"


@login_manager.user_loader
def load_user(user_id):

    return db.session.get(User, int(user_id))


# ==========================================
# DAILY MESSAGE RESET
# ==========================================

DAILY_LIMIT = 100


def reset_daily_messages(user):

    today = date.today()

    if (
        user.last_reset is None
        or user.last_reset.date() != today
    ):

        user.message_count = 0
        user.last_reset = datetime.utcnow()

        db.session.commit()

# ==========================================
# PRIVACY POLICY PAGE
# ==========================================

@app.route("/privacy")
def privacy():
    return render_template("privacy.html")

# ==========================================
# DATA DELETION INSTRUCTIONS PAGE
# ==========================================

@app.route("/data-deletion")
def data_deletion():
    return render_template("data-deletion.html")

# ==========================================
# TERMS OF SERVICE PAGE
# ==========================================

@app.route("/terms")
def terms():
    return render_template("terms.html")

# ==========================================
# HOME / LOGIN PAGE
# ==========================================

# ==========================================
# HOME / LOGIN PAGE
# ==========================================

@app.route("/")
def login():

    if current_user.is_authenticated:
        return redirect(url_for("chat"))

    return render_template("login.html")


# ==========================================
# GOOGLE AUTHENTICATION
# ==========================================

@app.route("/google_login")
def google_login():

    if not google.authorized:
        return redirect(url_for("google.login"))

    response = google.get("/oauth2/v2/userinfo")

    if not response.ok:
        return "Unable to retrieve Google account information.", 400

    info = response.json()

    google_id = info.get("id")
    email = info.get("email")
    name = info.get("name", "User")

    if not google_id or not email:
        return "Google account information is incomplete.", 400

    user = User.query.filter_by(
        google_id=google_id
    ).first()

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


# ==========================================
# LOGOUT
# ==========================================

@app.route("/logout")
@login_required
def logout():

    logout_user()

    return redirect(url_for("login"))


# ==========================================
# CHAT PAGE
# ==========================================

@app.route("/chat")
@login_required
def chat():

    reset_daily_messages(current_user)

    return render_template(
        "chat.html",
        user=current_user,
        message_count=current_user.message_count,
        limit=DAILY_LIMIT
    )


# ==========================================
# USER CHAT HISTORY
# ==========================================

@app.route("/chat_history")
@login_required
def chat_history():

    sessions = ChatSession.query.filter_by(
        user_id=current_user.id
    ).order_by(
        ChatSession.updated_at.desc()
    ).all()

    history = []

    for session in sessions:

        history.append({
            "id": session.id,
            "title": session.title,
            "created_at": session.created_at.strftime(
                "%Y-%m-%d %H:%M"
            ),
            "updated_at": session.updated_at.strftime(
                "%Y-%m-%d %H:%M"
            )
        })

    return jsonify({
        "history": history
    })


# ==========================================
# LOAD INDIVIDUAL CHAT SESSION
# ==========================================

@app.route("/chat_history/<int:session_id>")
@login_required
def load_chat_history(session_id):

    chat_session = ChatSession.query.filter_by(
        id=session_id,
        user_id=current_user.id
    ).first()

    if not chat_session:
        return jsonify({
            "error": "Chat session not found."
        }), 404

    conversations = Conversation.query.filter_by(
        chat_session_id=chat_session.id,
        user_id=current_user.id
    ).order_by(
        Conversation.created_at.asc()
    ).all()

    messages = []

    for conversation in conversations:

        messages.append({
            "user_message": conversation.user_message,
            "bot_response": conversation.bot_response,
            "created_at": conversation.created_at.strftime(
                "%Y-%m-%d %H:%M"
            )
        })

    return jsonify({
        "session_id": chat_session.id,
        "title": chat_session.title,
        "messages": messages
    })


# ==========================================
# SETTINGS PAGE
# ==========================================

@app.route("/settings", methods=["GET", "POST"])
@login_required
def settings():

    integration = Integration.query.filter_by(
        user_id=current_user.id
    ).first()

    if request.method == "POST":

        whatsapp_number = request.form.get(
            "whatsapp_number"
        )

        whatsapp_api_key = request.form.get(
            "whatsapp_api_key"
        )

        store_type = request.form.get(
            "store_type"
        )

        store_url = request.form.get(
            "store_url"
        )

        store_api_key = request.form.get(
            "store_api_key"
        )

        store_api_secret = request.form.get(
            "store_api_secret"
        )

        if not integration:

            integration = Integration(
                user_id=current_user.id
            )
            db.session.add(integration)

        configured_phone_number_id = os.getenv(
            "WHATSAPP_PHONE_NUMBER_ID"
        )

        if (
            not integration.whatsapp_phone_number_id
            and configured_phone_number_id
        ):
            integration.whatsapp_phone_number_id = (
                configured_phone_number_id
            )


            db.session.add(integration)

        integration.whatsapp_number = whatsapp_number
        if whatsapp_api_key:
            integration.whatsapp_api_key = whatsapp_api_key
        
        integration.store_type = store_type
        integration.store_url = store_url
        
        if store_api_key:
            integration.store_api_key = store_api_key
        if store_api_secret:
            integration.store_api_secret = store_api_secret          

        db.session.commit()

        return redirect(url_for("settings"))

    return render_template(
        "settings.html",
        integration=integration
    )


# ==========================================
# PREMIUM PAGE
# ==========================================

@app.route("/premium")
@login_required
def premium():

    return render_template("premium.html")


# ==========================================
# AI CHAT API
# ==========================================


@app.route("/send", methods=["POST"])
@login_required
def send_message():

    data = request.get_json(silent=True)

    if not data:
        return jsonify({
            "error": "Invalid request."
        }), 400

    user_message = data.get("message", "")

    if not isinstance(user_message, str):
        return jsonify({
            "error": "Message must be text."
        }), 400

    user_message = user_message.strip()

    if not user_message:
        return jsonify({
            "error": "Message cannot be empty."
        }), 400

    if len(user_message) > 10000:
        return jsonify({
            "error": "Message is too long."
        }), 400

    # Check requested chat session
    chat_session_id = data.get("chat_session_id")
    chat_session = None

    if chat_session_id is not None:

        try:
            chat_session_id = int(chat_session_id)
        except (TypeError, ValueError):
            return jsonify({
                "error": "Invalid chat session."
            }), 400

        chat_session = ChatSession.query.filter_by(
            id=chat_session_id,
            user_id=current_user.id
        ).first()

        if not chat_session:
            return jsonify({
                "error": "Chat session not found."
            }), 404

    # Reset daily message count if needed
    reset_daily_messages(current_user)

    # Check daily limit
    if current_user.message_count >= DAILY_LIMIT:
        return jsonify({
            "limit_reached": True,
            "message": "You have reached your daily limit of 100 messages."
        }), 403

        # Generate AI response
    try:
        integration = Integration.query.filter_by(
            user_id=current_user.id
        ).first()

        ai_reply = generate_response(
            user_message,
            store_url=integration.store_url if integration else None,
            consumer_key=integration.store_api_key if integration else None,
            consumer_secret=integration.store_api_secret if integration else None
        )

        if not ai_reply:
            raise Exception("Empty AI response")

    except Exception:
        app.logger.exception("AI response generation failed")

        return jsonify({
            "error": "Unable to generate an AI response. Please try again."
        }), 502

    # Save conversation and chat session
    try:

        # Create a new session if one was not supplied
        if not chat_session:

            chat_session = ChatSession(
                user_id=current_user.id,
                title=user_message[:200]
            )

            db.session.add(chat_session)
            db.session.flush()

        # Set title if this is an older unnamed session
        elif chat_session.title == "New Chat":

            chat_session.title = user_message[:200]

        conversation = Conversation(
            user_id=current_user.id,
            chat_session_id=chat_session.id,
            user_message=user_message,
            bot_response=ai_reply
        )

        db.session.add(conversation)

        current_user.message_count += 1

        db.session.commit()

    except Exception:

        db.session.rollback()

        app.logger.exception("Conversation database save failed")

        return jsonify({
            "error": "Unable to save your conversation."
        }), 500

    return jsonify({

        "reply": ai_reply,

        "chat_session_id": chat_session.id,

        "chat_title": chat_session.title,

        "message_count": current_user.message_count,

        "remaining_messages": DAILY_LIMIT - current_user.message_count,

        "limit": DAILY_LIMIT

    })

# ==========================================
# WHATSAPP MESSAGE SENDER
# ==========================================

def send_whatsapp_message(
    recipient,
    message,
    phone_number_id=None
):
    access_token = os.getenv("WHATSAPP_ACCESS_TOKEN")

    phone_number_id = (
        phone_number_id
        or os.getenv("WHATSAPP_PHONE_NUMBER_ID")
    )

    api_version = os.getenv(
        "WHATSAPP_API_VERSION",
        "v27.0"
    )

    if not access_token or not phone_number_id:
        raise RuntimeError(
            "WhatsApp credentials are missing."
        )

    url = (
        f"https://graph.facebook.com/"
        f"{api_version}/{phone_number_id}/messages"
    )

    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json"
    }

    payload = {
        "messaging_product": "whatsapp",
        "recipient_type": "individual",
        "to": recipient,
        "type": "text",
        "text": {
            "preview_url": False,
            "body": message[:4000]
        }
    }

    response = requests.post(
        url,
        headers=headers,
        json=payload,
        timeout=30
    )

    if not response.ok:
        app.logger.error(
            "WhatsApp API error: %s",
            response.text
        )
        response.raise_for_status()

    return response.json()

# ==========================================
# WHATSAPP WEBHOOK
# ==========================================

@app.route("/webhook", methods=["GET", "POST"])
def whatsapp_webhook():

    # Meta verification
    if request.method == "GET":

        mode = request.args.get("hub.mode")
        token = request.args.get("hub.verify_token")
        challenge = request.args.get("hub.challenge")

        expected_token = os.getenv("WHATSAPP_VERIFY_TOKEN")

        if (
            mode == "subscribe"
            and expected_token
            and token == expected_token
            and challenge
        ):
            return challenge, 200, {
                "Content-Type": "text/plain"
            }

        return "Webhook verification failed", 403

    # Receive incoming WhatsApp messages
    data = request.get_json(silent=True) or {}

    try:

        for entry in data.get("entry", []):

            for change in entry.get("changes", []):

                value = change.get("value", {})

                metadata = value.get("metadata", {})

                incoming_phone_number_id = metadata.get(
                    "phone_number_id"
                )


                if not incoming_phone_number_id:
                    continue

                integration = Integration.query.filter_by(
                    whatsapp_phone_number_id=incoming_phone_number_id
                ).first()

                if not integration:
                    app.logger.warning(
                        "No registered integration found for incoming WhatsApp number."
                    )
                    continue

                messages = value.get("messages", [])

                for incoming in messages:

                    message_id = incoming.get("id")

                    if not message_id:
                        continue

                    sender = incoming.get("from")
                    message_type = incoming.get("type")

                    # Initial version supports text messages
                    if not sender or message_type != "text":
                        continue

                    user_message = incoming.get(
                        "text", {}
                    ).get("body", "").strip()

                    if not user_message:
                        continue

                    # Atomically register the WhatsApp message ID
                    try:
                        db.session.add(
                            WhatsAppProcessedMessage(
                                message_id=message_id
                            )
                        )
                        db.session.commit()

                    except IntegrityError:
                        db.session.rollback()

                        app.logger.info(
                            "Duplicate WhatsApp message ignored."
                        )
                        continue

                    app.logger.info(
                        "Incoming WhatsApp text message received."
                    )

                                       # Generate AI response
                    ai_reply = generate_response(
                        user_message,
                        store_url=integration.store_url if integration else None,
                        consumer_key=integration.store_api_key if integration else None,
                        consumer_secret=integration.store_api_secret if integration else None
                    )
                    
                    if not ai_reply:
                        raise RuntimeError(
                            "AI returned an empty response."
                        )

                    # Save WhatsApp conversation

                    conversation = WhatsAppConversation(
                        owner_user_id=integration.user_id,
                        sender_id=sender,
                        user_message=user_message,
                        bot_response=ai_reply
                    )


                    db.session.add(conversation)
                    db.session.commit()

                    # Send AI response to WhatsApp
                    
                    send_whatsapp_message(
                        sender,
                        ai_reply,
                        phone_number_id=incoming_phone_number_id
                    )

        return "EVENT_RECEIVED", 200

    except Exception:

        db.session.rollback()

        app.logger.exception(
            "WhatsApp message processing failed."
        )

        return "EVENT_RECEIVED", 200

# ==========================================
# APPLICATION START
# ==========================================

if __name__ == "__main__":

    port = int(os.environ.get("PORT", 5000))

    app.run(
        host="0.0.0.0",
        port=port,
        debug=os.environ.get("FLASK_DEBUG", "false").lower() == "true"
    )
