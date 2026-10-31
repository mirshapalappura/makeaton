from flask import Blueprint, request, jsonify, session
from database import get_db

payments = Blueprint("payments", __name__, url_prefix="/api/payments")


@payments.route("", methods=["GET"])
def list_payments():
    if "user_id" not in session:
        return jsonify({"error": "Login required"}), 401

    db = get_db()

    if session["role"] in ("admin", "staff"):
        rows = db.execute("""
            SELECT p.*, i.total
            FROM payments p
            JOIN invoices i ON p.invoice_id = i.id
            ORDER BY p.id DESC
        """).fetchall()
    else:
        rows = db.execute("""
            SELECT p.*, i.total
            FROM payments p
            JOIN invoices i ON p.invoice_id = i.id
            JOIN subscriptions s ON i.subscription_id = s.id
            WHERE s.user_id = ?
            ORDER BY p.id DESC
        """, (session["user_id"],)).fetchall()

    db.close()
    return jsonify([dict(row) for row in rows])


@payments.route("", methods=["POST"])
def add_payment():
    if session.get("role") not in ("admin", "staff"):
        return jsonify({"error": "Staff access required"}), 403

    data = request.get_json() or {}

    try:
        invoice_id = int(data["invoice_id"])
        amount = round(float(data["amount"]), 2)
        method = data.get("payment_method", "UPI")

        if amount <= 0:
            raise ValueError()

    except (KeyError, ValueError, TypeError):
        return jsonify({"error": "Invalid payment details"}), 400

    db = get_db()

    invoice = db.execute("""
        SELECT * FROM invoices WHERE id = ?
    """, (invoice_id,)).fetchone()

    if not invoice:
        db.close()
        return jsonify({"error": "Invoice not found"}), 404

    balance = round(invoice["total"] - invoice["paid_amount"], 2)

    if amount > balance:
        db.close()
        return jsonify({"error": "Payment exceeds outstanding balance"}), 400

    db.execute("""
        INSERT INTO payments (invoice_id, amount, payment_method)
        VALUES (?, ?, ?)
    """, (invoice_id, amount, method))

    paid = round(invoice["paid_amount"] + amount, 2)
    status = "Paid" if paid >= invoice["total"] else "Partial"

    db.execute("""
        UPDATE invoices
        SET paid_amount = ?, status = ?
        WHERE id = ?
    """, (paid, status, invoice_id))

    db.commit()
    db.close()

    return jsonify({"message": "Payment recorded", "status": status}), 201