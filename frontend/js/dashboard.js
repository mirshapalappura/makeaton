async function loadDashboard() {
    try {
        const data = await api("/api/dashboard");

        document.getElementById("active").textContent =
            data.active_subscriptions;

        document.getElementById("customers").textContent =
            data.customers;

        document.getElementById("revenue").textContent =
            "₹" + data.revenue.toFixed(2);

        document.getElementById("outstanding").textContent =
            "₹" + data.outstanding.toFixed(2);

        document.getElementById("overdue").textContent =
            data.overdue_invoices;

    } catch (error) {
        alert(error.message);
    }
}

if (document.getElementById("active")) {
    loadDashboard();
}