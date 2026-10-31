// frontend/js/auth.js

const loginForm = document.getElementById("loginForm");

if (loginForm) {
    loginForm.addEventListener("submit", async (event) => {
        event.preventDefault();

        const email = document.getElementById("email").value.trim();
        const password = document.getElementById("password").value;
        const message = document.getElementById("message");

        try {
            const result = await API.login({ email, password });

            message.textContent = "Login successful!";
            message.className = "text-success mt-3";

            const role = result.user.role;

            if (role === "admin") {
                window.location.href = "/admin-dashboard.html";
            } else if (role === "staff") {
                window.location.href = "/staff-dashboard.html";
            } else if (role === "customer") {
                window.location.href = "/customer-dashboard.html";
            } else {
                message.textContent = "Unknown user role.";
            }

        } catch (error) {
            message.textContent = error.message;
            message.className = "text-danger mt-3";
        }
    });
}


// REGISTRATION

const registerForm = document.getElementById("registerForm");

if (registerForm) {
    registerForm.addEventListener("submit", async (event) => {
        event.preventDefault();

        const name = document.getElementById("name").value.trim();
        const email = document.getElementById("email").value.trim();
        const password = document.getElementById("password").value;
        const message = document.getElementById("message");

        try {
            await API.register({ name, email, password });

            message.textContent = "Registration successful!";
            message.className = "text-success mt-3";

            setTimeout(() => {
                window.location.href = "/login.html";
            }, 1000);

        } catch (error) {
            message.textContent = error.message;
            message.className = "text-danger mt-3";
        }
    });
}