from pathlib import Path
from flask import Flask, send_from_directory

from .config import Config
from .auth import auth
from .products import products
from .subscriptions import subscriptions
from .invoices import invoices
from .payments import payments

BASE_DIR = Path(__file__).resolve().parent.parent
FRONTEND_DIR = BASE_DIR / "frontend"


def create_app():
    app = Flask(
        __name__,
        static_folder=str(FRONTEND_DIR),
        static_url_path=""
    )

    app.config.from_object(Config)

    # Register backend APIs
    app.register_blueprint(auth)
    app.register_blueprint(products)
    app.register_blueprint(subscriptions)
    app.register_blueprint(invoices)
    app.register_blueprint(payments)

    # Open the frontend
    @app.route("/")
    def home():
        return send_from_directory(FRONTEND_DIR, "login.html")

    # Serve frontend HTML pages
    @app.route("/<page>.html")
    def html_page(page):
        return send_from_directory(FRONTEND_DIR, f"{page}.html")

    return app


app = create_app()

if __name__ == "__main__":
    app.run(debug=app.config["DEBUG"])