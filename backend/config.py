import os

# Main project directory
BASE_DIR = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "..")
)

class Config:
    # Flask secret key
    SECRET_KEY = os.environ.get(
        "SECRET_KEY",
        "development-only-change-this"
    )

    # SQLite database location
    DATABASE = os.path.join(BASE_DIR, "makeaton.db")

    # Debug mode
    DEBUG = os.environ.get("FLASK_DEBUG") == "1"