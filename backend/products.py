from flask import Blueprint, request, jsonify, session
from .database import get_db

products = Blueprint("products", __name__, url_prefix="/api/products")


@products.route("", methods=["GET"])
def list_products():
    db = get_db()
    rows = db.execute("SELECT * FROM products ORDER BY id DESC").fetchall()
    db.close()
    return jsonify([dict(row) for row in rows])


@products.route("", methods=["POST"])
def create_product():
    if session.get("role") not in ("admin", "staff"):
        return jsonify({"error": "Access denied"}), 403

    data = request.get_json() or {}

    try:
        name = data["name"].strip()
        price = float(data["price"])
        tax_rate = float(data.get("tax_rate", 18))

        if not name or price < 0 or not 0 <= tax_rate <= 100:
            raise ValueError()

    except (KeyError, ValueError, TypeError):
        return jsonify({"error": "Invalid product details"}), 400

    db = get_db()
    db.execute(
        """INSERT INTO products (name, description, price, tax_rate)
           VALUES (?, ?, ?, ?)""",
        (name, data.get("description", ""), price, tax_rate)
    )
    db.commit()
    db.close()

    return jsonify({"message": "Product created"}), 201


@products.route("/<int:product_id>", methods=["DELETE"])
def delete_product(product_id):
    if session.get("role") != "admin":
        return jsonify({"error": "Admin access required"}), 403

    db = get_db()
    db.execute("DELETE FROM products WHERE id = ?", (product_id,))
    db.commit()
    db.close()

    return jsonify({"message": "Product deleted"})