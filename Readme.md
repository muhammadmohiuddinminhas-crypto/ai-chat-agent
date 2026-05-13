# 🤖 AI Chat Agent (Flask Web Application)

---

## 📌 Project Overview

This is a full-stack AI Chat Agent built using Flask.  
It allows users to chat with an AI assistant, authenticate via Google Login, and stores conversation history in a database.

The system is also designed for future integrations like WhatsApp and e-commerce APIs.

---

## 🚀 Features

- 🔐 Google OAuth Login Authentication  
- 💬 AI Chat Interface  
- 🧠 AI Response Generation System  
- 🗂️ Conversation History Storage  
- 👤 User Session Management  
- ⚙️ Integration Settings (WhatsApp / Store APIs)  
- ☁️ Ready for Deployment (Railway / Render / Heroku)

---

## 🛠️ Tech Stack

- Python 🐍  
- Flask 🌐  
- Flask-Login 🔐  
- Flask-SQLAlchemy 🗄️  
- SQLite (Database)  
- HTML / CSS / JavaScript  
- OAuth 2.0 (Google Login)

---

## 📁 Project Structure

```
chat-agent/
│
├── app.py
├── ai.py
├── auth.py
├── config.py
├── database.py
├── requirements.txt
│
├── templates/
│   ├── login.html
│   ├── chat.html
│   └── settings.html
│
├── static/
│   ├── css/
│   └── js/
```

---

## ⚙️ Installation & Setup

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

## 🗄️ Database

The project uses SQLite with the following tables:

- Users  
- Conversations  
- Integrations  

The database is automatically created on first run.

---

## ☁️ Deployment

This project is deployment-ready for:

- Railway 🚄  
- Render 🌐  
- Heroku ☁️  

---

## 🎯 Future Improvements

- WhatsApp chatbot integration  
- Payment system integration  
- Multi-language support  
- AI model switching (OpenAI / Groq / Cerebras)  
- Admin dashboard  

---

## 👨‍💻 Author

Developed as a Final Year Project  
Focused on AI integration + web automation  

---

## 📜 License

This project is for educational purposes only.