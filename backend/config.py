import os

# Get the main project directory
BASE_DIR = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "..")
)

class Config:
    SECRET_KEY = os.environ.get(
        "SECRET_KEY", "development-only-change-this"
    )

    DATABASE = os.path.join(BASE_DIR, "makeaton.db")

    DEBUG = os.environ.get("FLASK_DEBUG") == "1"