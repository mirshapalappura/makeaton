// frontend/js/api.js

const API_BASE = "/api";

async function apiRequest(endpoint, options = {}) {
    const response = await fetch(`${API_BASE}${endpoint}`, {
        ...options,
        credentials: "same-origin",
        headers: {
            "Content-Type": "application/json",
            ...options.headers
        }
    });

    const data = await response.json();

    if (!response.ok) {
        throw new Error(data.error || "Something went wrong");
    }

    return data;
}

// Authentication
const API = {
    register: (data) =>
        apiRequest("/auth/register", {
            method: "POST",
            body: JSON.stringify(data)
        }),

    login: (data) =>
        apiRequest("/auth/login", {
            method: "POST",
            body: JSON.stringify(data)
        }),

    currentUser: () =>
        apiRequest("/auth/me"),

    logout: () =>
        apiRequest("/auth/logout", {
            method: "POST"
        }),

    // Products
    getProducts: () =>
        apiRequest("/products"),

    addProduct: (data) =>
        apiRequest("/products", {
            method: "POST",
            body: JSON.stringify(data)
        }),

    deleteProduct: (id) =>
        apiRequest(`/products/${id}`, {
            method: "DELETE"
        }),

    // Subscriptions
    getSubscriptions: () =>
        apiRequest("/subscriptions"),

    createSubscription: (data) =>
        apiRequest("/subscriptions", {
            method: "POST",
            body: JSON.stringify(data)
        }),

    updateSubscription: (id, status) =>
        apiRequest(`/subscriptions/${id}/status`, {
            method: "PUT",
            body: JSON.stringify({ status })
        }),

    // Invoices
    getInvoices: () =>
        apiRequest("/invoices"),

    generateInvoices: () =>
        apiRequest("/invoices/generate", {
            method: "POST"
        }),

    // Payments
    getPayments: () =>
        apiRequest("/payments"),

    addPayment: (data) =>
        apiRequest("/payments", {
            method: "POST",
            body: JSON.stringify(data)
        })
};