CREATE TABLE user (
    id INTEGER PRIMARY KEY AUTOINCREMENT,

    google_id TEXT UNIQUE,

    email TEXT UNIQUE,

    name TEXT,

    message_count INTEGER DEFAULT 0,

    last_reset DATETIME
);



CREATE TABLE conversation (
    id INTEGER PRIMARY KEY AUTOINCREMENT,

    user_id INTEGER,

    user_message TEXT,

    bot_reply TEXT,

    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);



CREATE TABLE integration (
    id INTEGER PRIMARY KEY AUTOINCREMENT,

    user_id INTEGER,

    whatsapp_number TEXT,

    whatsapp_api_key TEXT,

    store_type TEXT,

    store_url TEXT,

    store_api_key TEXT
);