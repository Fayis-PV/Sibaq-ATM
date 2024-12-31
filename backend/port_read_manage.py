import threading
import time
import random
from queue import Queue

# Create a shared queue to act as the "serial connection"
serial_queue = Queue()

# Arduino simulator function
def fake_arduino():
    print("Fake Arduino Simulator started.")
    while True:
        # Simulate button press: randomly send "1" or "0"
        button_state = random.choice(["1", "0"])
        serial_queue.put(button_state)  # Send data to the queue
        print(f"Simulator sent: {button_state}")
        time.sleep(1)  # Wait for 1 second before sending next data

# Serial reader function
def serial_reader():
    print("Serial Reader started.")
    while True:
        if not serial_queue.empty():
            # Read data from the queue
            data = serial_queue.get()
            print(f"Reader received: {data}")

# Create threads for the simulator and reader
simulator_thread = threading.Thread(target=fake_arduino, daemon=True)
reader_thread = threading.Thread(target=serial_reader, daemon=True)

# Start the threads
simulator_thread.start()
reader_thread.start()

# Keep the main program running to allow threads to run
try:
    while True:
        time.sleep(0.1)  # Keep the program alive
except KeyboardInterrupt:
    print("Simulation stopped.")
