import threading
import time
from queue import Queue
import requests

# Shared queue to simulate serial communication (button state)
serial_queue = Queue()

# Simulated Arduino input: Card inserted (1) or card removed (0)
def fake_arduino():
    """
    Simulates Arduino input: '1' for card inserted, '0' for card removed.
    Randomly changes between 1 and 0.
    """
    print("[Fake Arduino Simulator] Started.")
    while True:
        button_state = "1" if time.time() % 10 < 5 else "0"  # Simulate card insert/remove
        serial_queue.put(button_state)
        time.sleep(0.1)

# API Functions
def leaderboard():
    """
    Fetches the leaderboard information via the API and displays it.
    """
    try:
        api_endpoint = "http://localhost:5000/leaderboard"
        response = requests.get(api_endpoint)
        if response.status_code == 200:
            data = response.json()
            print("[Leaderboard] Data fetched successfully:")
            print(data)
        else:
            print("[Leaderboard] Failed to fetch data.")
    except Exception as e:
        print(f"[Leaderboard] Error: {e}")

def candidate_detail(chest_no):
    """
    Fetches candidate details based on the chest number.
    """
    try:
        api_endpoint = "http://localhost:5000/process_barcode"
        response = requests.post(api_endpoint, json={"barcode": chest_no})
        data = response.json()
        if data["status"] == "success":
            print(f"[Candidate Details] {data['message']}")
        else:
            print(f"[Candidate Details] {data['message']}")
    except Exception as e:
        print(f"[Candidate Details] Error: {e}")

# Simulate barcode input for testing
def simulate_barcode_input():
    """
    Simulates the barcode input. Sometimes it returns a valid barcode,
    and sometimes it returns an empty string to simulate failure.
    """
    # Simulate success or failure randomly
    if time.time() % 2 == 0:
        return "123456789012"  # Valid barcode
    else:
        return ""  # Simulate no barcode

# Main function to manage card state and barcode handling
def manage_card_state():
    """
    Manages the card state (inserted/removed) and handles the barcode input process.
    """
    print("[ATM Simulation] Started.")
    current_state = "0"  # Initial state (card not inserted)

    while True:
        if not serial_queue.empty():
            new_state = serial_queue.get()  # Read the latest button state
            if new_state != current_state:  # Only process if state changes
                current_state = new_state
                if current_state == "1":  # Card inserted
                    print("[Card Inserted] Waiting for barcode...")
                    timeout = 10  # Timeout for barcode scanning
                    start_time = time.time()

                    # Start barcode scanning process
                    while time.time() - start_time < timeout:
                        # Check if card is removed during barcode waiting
                        if not serial_queue.empty():
                            new_state = serial_queue.get()
                            if new_state == "0":  # Card removed
                                print("[Card Removed During Barcode Waiting] Showing leaderboard.")
                                leaderboard()
                                break

                        # Simulate manual barcode input (test function)
                        barcode = simulate_barcode_input()
                        print(f"[Scanner] Barcode input: {barcode}")

                        if barcode and len(barcode) == 12:  # Check if barcode is valid (12 digits)
                            chest_no = barcode[:4]  # Extract chest number
                            candidate_detail(chest_no)  # Fetch candidate details
                            break
                        elif barcode == "":
                            print("[Error] No barcode detected within timeout. Please try again.")
                            break
                        else:
                            print("[Error] Invalid barcode. Please try again.")

                    else:
                        print("[Error] Barcode not detected or invalid within timeout.")
                elif current_state == "0":  # Card removed
                    print("[Card Removed] Showing leaderboard.")
                    leaderboard()

        time.sleep(0.1)  # Check for new state every 100ms

# Threads for Arduino simulation and card state management
simulator_thread = threading.Thread(target=fake_arduino, daemon=True)
card_manager_thread = threading.Thread(target=manage_card_state, daemon=True)

# Start threads
simulator_thread.start()
card_manager_thread.start()

# Keep the main program running
try:
    while True:
        time.sleep(0.1)  # Keep the program alive
except KeyboardInterrupt:
    print("[Simulation Stopped]")
