async function loadProducts() {
    const products = await api("/api/products");

    const table = document.getElementById("product-list");

    table.innerHTML = products.map(product => `
        <tr>
            <td>${product.name}</td>
            <td>${product.description || ""}</td>
            <td>₹${product.price}</td>
            <td>${product.tax_rate}%</td>
        </tr>
    `).join("");
}

async function addProduct() {
    try {
        await api("/api/products", "POST", {
            name: document.getElementById("product-name").value,
            description: document.getElementById("description").value,
            price: document.getElementById("price").value,
            tax_rate: document.getElementById("tax").value
        });

        alert("Product added");
        loadProducts();

    } catch (error) {
        alert(error.message);
    }
}

if (document.getElementById("product-list")) {
    loadProducts();
}