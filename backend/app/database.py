import sqlite3
import os

# Pointing directly to the database file created by seed.py
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
DB_PATH = os.path.join(BASE_DIR, "database", "care.db")

def get_db_connection():
    """Establishes connection to care.db with Row access by column name."""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row  # Enables dict-like access: row["user_id"]
    conn.execute("PRAGMA foreign_keys = ON;")
    return conn