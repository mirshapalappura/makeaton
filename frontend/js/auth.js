// frontend/js/auth.js

// LOGIN
const loginForm = document.getElementById("loginForm");

if (loginForm) {
    loginForm.addEventListener("submit", async (event) => {
        event.preventDefault();

        const email = document.getElementById("email").value;
        const password = document.getElementById("password").value;
        const message = document.getElementById("message");

        try {
            const result = await API.login({
                email,
                password
            });

            message.textContent = result.message;

            // Go to dashboard after successful login
            window.location.href = "/dashboard.html";

        } catch (error) {
            message.textContent = error.message;
        }
    });
}


// REGISTRATION
const registerForm = document.getElementById("registerForm");

if (registerForm) {
    registerForm.addEventListener("submit", async (event) => {
        event.preventDefault();

        const name = document.getElementById("name").value;
        const email = document.getElementById("email").value;
        const password = document.getElementById("password").value;
        const message = document.getElementById("message");

        try {
            const result = await API.register({
                name,
                email,
                password
            });

            message.textContent = result.message;

            // Redirect to login
            window.location.href = "/login.html";

        } catch (error) {
            message.textContent = error.message;
        }
    });
}