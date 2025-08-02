import sqlite3
import os

# Ensure the data directory exists
os.makedirs("data", exist_ok=True)

DB_PATH = "data/health_tips.db"

def init_db():
    """Initialize the SQLite database and create necessary table."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # Table to store health tips (user input and bot-generated response)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS interactions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_input TEXT NOT NULL,
            bot_response TEXT,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
            upvotes INTEGER DEFAULT 0
        )
    """)

    conn.commit()
    conn.close()

def insert_tip(user_input, bot_response=None):
    """Insert a new health tip and optional bot response."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO interactions (user_input, bot_response)
        VALUES (?, ?)
    """, (user_input, bot_response))

    conn.commit()
    conn.close()

def get_all_tips():
    """Fetch all tips from the database sorted by latest timestamp."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("""
        SELECT id, user_input, bot_response, timestamp, upvotes
        FROM interactions
        ORDER BY timestamp DESC
    """)

    rows = cursor.fetchall()
    conn.close()
    return rows

def upvote_tip(tip_id):
    """Increment the upvote count for a given tip ID."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("""
        UPDATE interactions
        SET upvotes = upvotes + 1
        WHERE id = ?
    """, (tip_id,))

    conn.commit()
    conn.close()
