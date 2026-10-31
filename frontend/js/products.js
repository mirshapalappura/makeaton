// frontend/js/products.js

async function loadProducts() {
    const table = document.getElementById("productsTable");
    const message = document.getElementById("message");

    try {
        const products = await API.getProducts();

        table.innerHTML = "";

        if (products.length === 0) {
            message.textContent = "No products available.";
            return;
        }

        message.textContent = "";

        products.forEach((product) => {
            const row = document.createElement("tr");

            const values = [
                product.id,
                product.name,
                product.description || "",
                "₹" + Number(product.price).toFixed(2),
                product.tax_rate + "%"
            ];

            values.forEach((value) => {
                const cell = document.createElement("td");
                cell.textContent = value;
                row.appendChild(cell);
            });

            table.appendChild(row);
        });

    } catch (error) {
        message.textContent = "Error: " + error.message;
    }
}

loadProducts();