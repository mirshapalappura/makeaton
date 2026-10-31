import sqlite3
from flask import current_app, g


def get_db():
    """Connect to SQLite database."""

    if "db" not in g:
        g.db = sqlite3.connect(
            current_app.config["DATABASE"]
        )

        g.db.row_factory = sqlite3.Row
        g.db.execute("PRAGMA foreign_keys = ON")

    return g.db


def close_db(error=None):
    """Close the database connection."""

    db = g.pop("db", None)

    if db is not None:
        db.close()


def init_db():
    """Create the products table."""

    db = get_db()

    db.execute("""
        CREATE TABLE IF NOT EXISTS products (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            type TEXT NOT NULL,
            sales_price REAL NOT NULL CHECK(sales_price >= 0),
            cost_price REAL NOT NULL DEFAULT 0
                CHECK(cost_price >= 0),
            notes TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)

    db.commit()


def init_app(app):
    """Initialize database with Flask application."""

    app.teardown_appcontext(close_db)

    with app.app_context():
        init_db()