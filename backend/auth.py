from flask import Blueprint, request, jsonify, session
from werkzeug.security import generate_password_hash, check_password_hash
from .database import get_db

auth = Blueprint("auth", __name__, url_prefix="/api/auth")


@auth.route("/register", methods=["POST"])
def register():
    data = request.get_json() or {}

    name = data.get("name", "").strip()
    email = data.get("email", "").strip().lower()
    password = data.get("password", "")

    if not name or not email or len(password) < 8:
        return jsonify({"error": "Enter valid details. Password must have at least 8 characters."}), 400

    db = get_db()

    try:
        db.execute(
            "INSERT INTO users (name, email, password) VALUES (?, ?, ?)",
            (name, email, generate_password_hash(password))
        )
        db.commit()
        return jsonify({"message": "Registration successful"}), 201

    except Exception:
        return jsonify({"error": "Email already registered"}), 409

    finally:
        db.close()


@auth.route("/login", methods=["POST"])
def login():
    data = request.get_json() or {}

    email = data.get("email", "").strip().lower()
    password = data.get("password", "")

    db = get_db()
    user = db.execute(
        "SELECT * FROM users WHERE email = ?", (email,)
    ).fetchone()
    db.close()

    if not user or not check_password_hash(user["password"], password):
        return jsonify({"error": "Invalid email or password"}), 401

    session.clear()
    session["user_id"] = user["id"]
    session["role"] = user["role"]

    return jsonify({
        "message": "Login successful",
        "user": {
            "id": user["id"],
            "name": user["name"],
            "email": user["email"],
            "role": user["role"]
        }
    })


@auth.route("/me")
def me():
    if "user_id" not in session:
        return jsonify({"error": "Not logged in"}), 401

    db = get_db()

    user = db.execute(
        "SELECT id, name, email, role FROM users WHERE id = ?",
        (session["user_id"],)
    ).fetchone()

    db.close()

    if not user:
        session.clear()
        return jsonify({"error": "User not found"}), 401

    return jsonify(dict(user))


@auth.route("/logout", methods=["POST"])
def logout():
    session.clear()
    return jsonify({"message": "Logged out"})


@auth.route("/customers")
def customers():
    if session.get("role") not in ("admin", "staff"):
        return jsonify({"error": "Access denied"}), 403

    db = get_db()
    rows = db.execute(
        "SELECT id, name, email FROM users WHERE role = 'customer'"
    ).fetchall()
    db.close()

    return jsonify([dict(row) for row in rows])