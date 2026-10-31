from flask import Flask
from .config import Config
from .database import init_app
from .products import products_bp


def create_app():
    app = Flask(__name__)

    app.config.from_object(Config)

    init_app(app)

    app.register_blueprint(products_bp)

    @app.route("/")
    def home():
        return {
            "message": "Makeaton Subscription Management API",
            "status": "running"
        }

    return app


app = create_app()


if __name__ == "__main__":
    app.run(debug=app.config["DEBUG"])