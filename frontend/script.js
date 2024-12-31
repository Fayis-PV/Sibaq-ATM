const statusDiv = document.getElementById("status");
const barcodeInput = document.getElementById("barcode-input");

// WebSocket connection to the backend
const ws = new WebSocket("ws://localhost:6789");

ws.onmessage = function (event) {
    if (event.data === "true") {
        statusDiv.innerHTML = "Card detected! Please scan your barcode.";
        barcodeInput.style.display = "block"; // Show barcode input
    } else {
        statusDiv.innerHTML = "Waiting for card...";
        barcodeInput.style.display = "none"; // Hide barcode input
    }
};

// Handle barcode submission
barcodeInput.addEventListener("change", function () {
    const barcode = barcodeInput.value;
    fetch("http://localhost:5000/process_barcode", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ barcode }),
    })
        .then((response) => response.json())
        .then((data) => {
            alert(data.message);
            barcodeInput.value = ""; // Clear input after submission
        })
        .catch((error) => console.error("Error:", error));
});
