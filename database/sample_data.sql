INSERT OR IGNORE INTO products
(name, description, price, tax_rate)
VALUES
('Odoo ERP', 'ERP subscription product', 1000, 18),
('Extra Seat', 'Additional user seat', 200, 18),
('Cloud Storage', 'Cloud storage service', 500, 18);

INSERT OR IGNORE INTO plans
(name, price, billing_cycle, description)
VALUES
('Basic Monthly', 999, 'monthly', 'Monthly subscription'),
('Professional Yearly', 9999, 'yearly', 'Annual subscription'),
('Premium Monthly', 1999, 'monthly', 'Premium monthly plan');