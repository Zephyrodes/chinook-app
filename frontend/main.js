let tracks = [];
let cart = [];

const API_BASE = "http://44.200.147.21:8000/api";

window.onload = async function() {
    try {
        const res = await fetch(`${API_BASE}/tracks`);
        tracks = await res.json();
        renderTracks();
    } catch (err) {
        console.error("Error cargando tracks:", err);
    }
};

function renderTracks() {
    const container = document.getElementById("tracksContainer");
    container.innerHTML = "";
    tracks.forEach(track => {
        const card = document.createElement("div");
        card.className = "track-card";
        card.innerHTML = `
            <h3>${track.Name}</h3>
            <p>Precio: $${track.UnitPrice}</p>
            <input type="number" min="1" value="1" id="qty-${track.TrackId}">
            <button onclick="addToCart(${track.TrackId})">Agregar</button>
        `;
        container.appendChild(card);
    });
}

function addToCart(trackId) {
    const qty = parseInt(document.getElementById(`qty-${trackId}`).value);
    const existing = cart.find(item => item.track_id === trackId);
    if (existing) {
        existing.quantity += qty;
    } else {
        cart.push({ track_id: trackId, quantity: qty });
    }
    renderCart();
}

function renderCart() {
    const ul = document.getElementById("cart");
    ul.innerHTML = "";
    cart.forEach(item => {
        const track = tracks.find(t => t.TrackId === item.track_id);
        const li = document.createElement("li");
        li.textContent = `${track.Name} - Cantidad: ${item.quantity}`;
        ul.appendChild(li);
    });
}

document.getElementById("buyBtn").addEventListener("click", async () => {
    const customerId = parseInt(document.getElementById("customerId").value);
    if (!customerId) {
        alert("Ingresa un Customer ID válido");
        return;
    }

    const payload = {
        customer_id: customerId,
        billing_address: document.getElementById("billingAddress").value || undefined,
        billing_city: document.getElementById("billingCity").value || undefined,
        billing_country: document.getElementById("billingCountry").value || undefined,
        lines: cart
    };

    try {
        const res = await fetch(`${API_BASE}/purchase/buy`, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify(payload)
        });

        const data = await res.json();
        document.getElementById("result").textContent = JSON.stringify(data, null, 2);
        cart = [];
        renderCart();
    } catch (err) {
        console.error("Error al comprar:", err);
        alert("Error en la compra");
    }
});
