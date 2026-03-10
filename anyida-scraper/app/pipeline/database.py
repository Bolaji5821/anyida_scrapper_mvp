import sqlite3
import os
from contextlib import contextmanager
from app.utils.logger import logger

DB_PATH = os.path.join("data", "anyida.db")

def init_db():
    """
    Initializes the SQLite database and creates tables if they don't exist.
    """
    logger.info(f"Initializing database at {DB_PATH}")
    
    # Ensure data directory exists
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    # Create listings table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS listings (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT,
            price TEXT,
            location TEXT,
            link TEXT UNIQUE,
            scraped_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            source TEXT
        )
    ''')
    
    conn.commit()
    conn.close()
    logger.info("Database initialized successfully.")

@contextmanager
def get_db_connection():
    """
    Context manager for database connections.
    """
    conn = sqlite3.connect(DB_PATH)
    try:
        yield conn
    finally:
        conn.close()
