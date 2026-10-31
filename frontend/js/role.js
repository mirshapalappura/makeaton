// frontend/js/role.js

async function checkRole(allowedRoles) {
    try {
        const user = await API.currentUser();

        if (!allowedRoles.includes(user.role)) {
            window.location.replace("/login.html");
            return null;
        }

        const welcome = document.getElementById("welcome");

        if (welcome) {
            welcome.textContent = `Welcome, ${user.name}`;
        }

        return user;

    } catch (error) {
        window.location.replace("/login.html");
        return null;
    }
}

async function logout() {
    try {
        await API.logout();
        window.location.replace("/login.html");
    } catch (error) {
        alert(error.message);
    }
}