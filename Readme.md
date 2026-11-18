# ðŸ¤– AI Chat Agent (Flask Web Application)

---

## ðŸ“Œ Project Overview

This is a full-stack AI Chat Agent built using Flask.
It allows users to chat with an AI assistant, authenticate via Google Login, and stores conversation history in a database.

The system is also designed for future integrations like WhatsApp and e-commerce APIs.

---

## ðŸš€ Features

- ðŸ” Google OAuth Login Authentication
- ðŸ’¬ AI Chat Interface
- ðŸ§  AI Response Generation System
- ðŸ—‚ï¸ Conversation History Storage
- ðŸ‘¤ User Session Management
- âš™ï¸ Integration Settings (WhatsApp / Store APIs)
- â˜ï¸ Ready for Deployment (Railway / Render / Heroku)

---

## ðŸ› ï¸ Tech Stack

- Python ðŸ
- Flask ðŸŒ
- Flask-Login ðŸ”
- Flask-SQLAlchemy ðŸ—„ï¸
- SQLite (Database)
- HTML / CSS / JavaScript
- OAuth 2.0 (Google Login)

---

## ðŸ“ Project Structure

```
chat-agent/
â”‚
â”œâ”€â”€ app.py
â”œâ”€â”€ ai.py
â”œâ”€â”€ auth.py
â”œâ”€â”€ config.py
â”œâ”€â”€ database.py
â”œâ”€â”€ requirements.txt
â”‚
â”œâ”€â”€ templates/
â”‚   â”œâ”€â”€ login.html
â”‚   â”œâ”€â”€ chat.html
â”‚   â””â”€â”€ settings.html
â”‚
â”œâ”€â”€ static/
â”‚   â”œâ”€â”€ css/
â”‚   â””â”€â”€ js/
```

---

## âš™ï¸ Installation & Setup

### 1. Clone Repository

```bash
git clone https://github.com/your-username/chat-agent.git
cd chat-agent
```

---

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

---

### 3. Set Environment Variables

Create a `.env` file:

```env
SECRET_KEY=your_secret_key
GPT_API_KEY=your_api_key
GOOGLE_CLIENT_ID=your_google_client_id
GOOGLE_CLIENT_SECRET=your_google_client_secret
```

---

### 4. Run the Application

```bash
python app.py
```

Then open in browser:

```
http://127.0.0.1:5000
```

---

## ðŸ—„ï¸ Database

The project uses SQLite with the following tables:

- Users
- Conversations
- Integrations

The database is automatically created on first run.

---

## â˜ï¸ Deployment

This project is deployment-ready for:

- Railway ðŸš„
- Render ðŸŒ
- Heroku â˜ï¸

---

## ðŸŽ¯ Future Improvements

- WhatsApp chatbot integration
- Payment system integration
- Multi-language support
- AI model switching (OpenAI / Groq / Cerebras)
- Admin dashboard

---

## ðŸ‘¨â€ðŸ’» Author

Developed as a Final Year Project
Focused on AI integration + web automation

---

## ðŸ“œ License

This project is for educational purposes only.
