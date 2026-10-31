async function loadPlans() {
    const plans = await api("/api/plans");

    const select = document.getElementById("plan-id");

    if (!select) return;

    select.innerHTML = plans.map(plan => `
        <option value="${plan.id}">
            ${plan.name} - ₹${plan.price} (${plan.billing_cycle})
        </option>
    `).join("");
}

async function createSubscription() {
    try {
        await api("/api/subscriptions", "POST", {
            plan_id: document.getElementById("plan-id").value
        });

        alert("Subscription created");
        loadSubscriptions();

    } catch (error) {
        alert(error.message);
    }
}

async function loadSubscriptions() {
    const subscriptions = await api("/api/subscriptions");

    const table = document.getElementById("subscription-list");

    if (!table) return;

    table.innerHTML = subscriptions.map(sub => `
        <tr>
            <td>${sub.id}</td>
            <td>${sub.plan_name}</td>
            <td>${sub.status}</td>
            <td>
                ${sub.status !== "Active" ? `
                    <button class="btn btn-sm btn-primary"
                    onclick="changeStatus(${sub.id}, 'Active')">
                    Activate</button>` : ""}
            </td>
        </tr>
    `).join("");
}

async function changeStatus(id, status) {
    try {
        await api(`/api/subscriptions/${id}/status`, "PUT", { status });
        loadSubscriptions();
    } catch (error) {
        alert(error.message);
    }
}

if (document.getElementById("plan-id")) {
    loadPlans();
}

if (document.getElementById("subscription-list")) {
    loadSubscriptions();
}