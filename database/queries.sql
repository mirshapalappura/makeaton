-- List all active subscriptions
SELECT * FROM subscriptions
WHERE status = 'Active';

-- List unpaid invoices
SELECT * FROM invoices
WHERE status != 'Paid';

-- Total revenue
SELECT COALESCE(SUM(amount), 0) AS revenue
FROM payments;

-- Customer subscription history
SELECT s.*, p.name AS plan_name
FROM subscriptions s
JOIN plans p ON s.plan_id = p.id
WHERE s.user_id = ?;

-- Overdue invoices
SELECT * FROM invoices
WHERE status != 'Paid'
AND due_date < DATE('now');