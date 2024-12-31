import requests
import time

# Simulate barcode scanning
def simulate_barcode_scan():
    while True:
        barcode = input("Enter a barcode: ")  # Mock scanner input
        response = requests.post(
            "http://localhost:5000/process_barcode",
            json={"barcode": barcode},
        )
        print(response.json())

if __name__ == "__main__":
    simulate_barcode_scan()
