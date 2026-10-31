import sqlite3
import os
from pathlib import Path
from werkzeug.security import generate_password_hash
from .config import Config

DATABASE = Config.DATABASE

BASE_DIR = Path(__file__).resolve().parent.parent
SCHEMA_PATH = BASE_DIR / "database" / "schema.sql"
SAMPLE_PATH = BASE_DIR / "database" / "sample_data.sql"


def get_db():
    connection = sqlite3.connect(DATABASE, timeout=10)
    connection.row_factory = sqlite3.Row
    connection.execute("PRAGMA foreign_keys = ON")
    return connection


def init_db():
    os.makedirs(os.path.dirname(os.path.abspath(DATABASE)), exist_ok=True)

    db = get_db()

    with open(SCHEMA_PATH, encoding="utf-8") as f:
        db.executescript(f.read())

    with open(SAMPLE_PATH, encoding="utf-8") as f:
        db.executescript(f.read())

    admin = db.execute(
        "SELECT id FROM users WHERE email = ?",
        ("admin@brightloop.com",)
    ).fetchone()

    if not admin:
        db.execute("""
            INSERT INTO users (name, email, password, role)
            VALUES (?, ?, ?, ?)
        """, (
            "Brightloop Admin",
            "admin@brightloop.com",
            generate_password_hash("Admin@12345"),
            "admin"
        ))

    db.commit()
    db.close()

    print("Database initialized successfully!")


if __name__ == "__main__":
    init_db()