import sqlite3
import os
from werkzeug.security import generate_password_hash
from config import Config
DATABASE = Config.DATABASE


def get_db():
    connection = sqlite3.connect(DATABASE, timeout=10)
    connection.row_factory = sqlite3.Row
    connection.execute("PRAGMA foreign_keys = ON")
    return connection


def init_db():
    os.makedirs(os.path.dirname(DATABASE), exist_ok=True)

    db = get_db()

    base_dir = os.path.dirname(DATABASE)

    with open(os.path.join(base_dir, "schema.sql"), encoding="utf-8") as f:
        db.executescript(f.read())

    with open(os.path.join(base_dir, "sample_data.sql"), encoding="utf-8") as f:
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
    if __name__ == "__main__":
        init_db()
        print("Database initialized successfully!")