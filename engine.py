import sqlite3
import os
from contextlib import contextmanager

from config import logger

DB_FILE = "db.sqlite3"


# инитер db
def init_db():
    if os.path.exists(DB_FILE):
        logger.info("Database is initialized")
        return

    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()

    # table reduction url
    cursor.execute("""
        CREATE TABLE reduction_url_model (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            idempotency_key TEXT NOT NULL UNIQUE,
            url TEXT NOT NULL,
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP
        );
    """)

    # pool key
    cursor.execute("""
        CREATE TABLE idempotency_pool (
            key TEXT PRIMARY KEY,
            status TEXT NOT NULL CHECK(status IN ('available','reserved','used')),
            reserved_at DATETIME
        );
    """)

    conn.commit()
    conn.close()
    logger.info("Database initialized successfully")


# --- выдача сессий и отлов первичных except
@contextmanager
def get_db():
    conn = sqlite3.connect(DB_FILE)
    try:
        yield conn
        conn.commit()
    except:
        conn.rollback()
        raise
    finally:
        conn.close()


# --- вызываем инициализацию при импорте ---
init_db()
