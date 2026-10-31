from flask import Blueprint, request, jsonify, session
from database import get_db
from datetime import date, timedelta
import calendar

subscriptions = Blueprint(
    "subscriptions", __name__, url_prefix="/api/subscriptions"
)


def add_months(original_date, months):
    month = original_date.month - 1 + months
    year = original_date.year + month // 12
    month = month % 12 + 1
    day = min(
        original_date.day,
        calendar.monthrange(year, month)[1]
    )
    return date(year, month, day)


@subscriptions.route("", methods=["GET"])
def list_subscriptions():
    if "user_id" not in session:
        return jsonify({"error": "Login required"}), 401

    db = get_db()

    if session["role"] in ("admin", "staff"):
        rows = db.execute("""
            SELECT s.*, u.name AS customer_name,
                   p.name AS plan_name, p.price
            FROM subscriptions s
            JOIN users u ON s.user_id = u.id
            JOIN plans p ON s.plan_id = p.id
            ORDER BY s.id DESC
        """).fetchall()
    else:
        rows = db.execute("""
            SELECT s.*, p.name AS plan_name, p.price
            FROM subscriptions s
            JOIN plans p ON s.plan_id = p.id
            WHERE s.user_id = ?
            ORDER BY s.id DESC
        """, (session["user_id"],)).fetchall()

    db.close()
    return jsonify([dict(row) for row in rows])


@subscriptions.route("", methods=["POST"])
def create_subscription():
    if "user_id" not in session:
        return jsonify({"error": "Login required"}), 401

    data = request.get_json() or {}
    role = session["role"]

    try:
        plan_id = int(data["plan_id"])
        user_id = int(data["user_id"]) if role in ("admin", "staff") else session["user_id"]
    except (KeyError, ValueError, TypeError):
        return jsonify({"error": "Invalid subscription details"}), 400

    db = get_db()

    plan = db.execute(
        "SELECT * FROM plans WHERE id = ?", (plan_id,)
    ).fetchone()

    customer = db.execute(
        "SELECT id FROM users WHERE id = ? AND role = 'customer'",
        (user_id,)
    ).fetchone()

    if not plan or not customer:
        db.close()
        return jsonify({"error": "Invalid plan or customer"}), 400

    db.execute("""
        INSERT INTO subscriptions (user_id, plan_id, status)
        VALUES (?, ?, 'Pending')
    """, (user_id, plan_id))

    db.commit()
    db.close()

    return jsonify({"message": "Subscription created"}), 201


@subscriptions.route("/<int:sub_id>/status", methods=["PUT"])
def update_status(sub_id):
    if session.get("role") not in ("admin", "staff"):
        return jsonify({"error": "Staff access required"}), 403

    data = request.get_json() or {}
    new_status = data.get("status")

    allowed = ("Confirmed", "Active", "Paused", "Cancelled")

    if new_status not in allowed:
        return jsonify({"error": "Invalid status"}), 400

    db = get_db()
    sub = db.execute("""
        SELECT s.*, p.billing_cycle
        FROM subscriptions s
        JOIN plans p ON s.plan_id = p.id
        WHERE s.id = ?
    """, (sub_id,)).fetchone()

    if not sub:
        db.close()
        return jsonify({"error": "Subscription not found"}), 404

    start_date = date.today()
    end_date = (
        add_months(start_date, 1)
        if sub["billing_cycle"] == "monthly"
        else add_months(start_date, 12)
    )

    if new_status == "Active":
        db.execute("""
            UPDATE subscriptions
            SET status = ?, start_date = ?, end_date = ?
            WHERE id = ?
        """, (new_status, start_date.isoformat(), end_date.isoformat(), sub_id))
    else:
        db.execute(
            "UPDATE subscriptions SET status = ? WHERE id = ?",
            (new_status, sub_id)
        )

    db.commit()
    db.close()

    return jsonify({"message": "Subscription updated"})