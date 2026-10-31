async function generateInvoices() {
    try {
        const result = await api("/api/invoices/generate", "POST");
        alert(result.message);
        loadInvoices();
    } catch (error) {
        alert(error.message);
    }
}

async function loadInvoices() {
    const invoices = await api("/api/invoices");

    const table = document.getElementById("invoice-list");

    if (!table) return;

    table.innerHTML = invoices.map(invoice => `
        <tr>
            <td>${invoice.id}</td>
            <td>₹${invoice.subtotal}</td>
            <td>₹${invoice.tax}</td>
            <td>₹${invoice.total}</td>
            <td>₹${invoice.paid_amount}</td>
            <td>${invoice.status}</td>
            <td>${invoice.due_date}</td>
        </tr>
    `).join("");
}

async function loadPayments() {
    const payments = await api("/api/payments");

    const table = document.getElementById("payment-list");

    if (!table) return;

    table.innerHTML = payments.map(payment => `
        <tr>
            <td>${payment.id}</td>
            <td>${payment.invoice_id}</td>
            <td>₹${payment.amount}</td>
            <td>${payment.payment_method}</td>
            <td>${payment.created_at}</td>
        </tr>
    `).join("");
}

async function addPayment() {
    try {
        await api("/api/payments", "POST", {
            invoice_id: document.getElementById("invoice-id").value,
            amount: document.getElementById("amount").value,
            payment_method: document.getElementById("method").value
        });

        alert("Payment recorded");
        loadPayments();
        loadInvoices();

    } catch (error) {
        alert(error.message);
    }
}

if (document.getElementById("invoice-list")) {
    loadInvoices();
}

if (document.getElementById("payment-list")) {
    loadPayments();
}