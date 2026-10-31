from flask import Blueprint, jsonify, session
from .database import get_db
from datetime import date, timedelta

invoices = Blueprint("invoices", __name__, url_prefix="/api/invoices")


@invoices.route("", methods=["GET"])
def list_invoices():
    if "user_id" not in session:
        return jsonify({"error": "Login required"}), 401

    db = get_db()

    if session["role"] in ("admin", "staff"):
        rows = db.execute("""
            SELECT i.*, u.name AS customer_name
            FROM invoices i
            JOIN subscriptions s ON i.subscription_id = s.id
            JOIN users u ON s.user_id = u.id
            ORDER BY i.id DESC
        """).fetchall()
    else:
        rows = db.execute("""
            SELECT i.*
            FROM invoices i
            JOIN subscriptions s ON i.subscription_id = s.id
            WHERE s.user_id = ?
            ORDER BY i.id DESC
        """, (session["user_id"],)).fetchall()

    db.close()
    return jsonify([dict(row) for row in rows])


@invoices.route("/generate", methods=["POST"])
def generate_invoices():
    if session.get("role") not in ("admin", "staff"):
        return jsonify({"error": "Staff access required"}), 403

    db = get_db()

    active = db.execute("""
        SELECT s.id, s.end_date, p.price, p.billing_cycle
        FROM subscriptions s
        JOIN plans p ON s.plan_id = p.id
        WHERE s.status = 'Active'
    """).fetchall()

    count = 0

    for sub in active:
        existing = db.execute("""
            SELECT id FROM invoices
            WHERE subscription_id = ?
            AND created_at >= DATE('now', 'start of month')
        """, (sub["id"],)).fetchone()

        if existing:
            continue

        subtotal = float(sub["price"])
        tax = round(subtotal * 0.18, 2)
        total = round(subtotal + tax, 2)

        db.execute("""
            INSERT INTO invoices
            (subscription_id, subtotal, tax, total, due_date)
            VALUES (?, ?, ?, ?, ?)
        """, (
            sub["id"], subtotal, tax, total,
            (date.today() + timedelta(days=7)).isoformat()
        ))

        count += 1

    db.commit()
    db.close()

    return jsonify({
        "message": f"{count} invoice(s) generated",
        "count": count
    })