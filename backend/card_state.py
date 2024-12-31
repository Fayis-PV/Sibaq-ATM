import serial
import requests
import serial.tools.list_ports

ports = serial.tools.list_ports.comports()
arduino_port = None

for port in ports:
    if "USB" in port.description:
        print(f"Arduino connected on port: {port.device}")
        arduino_port = port.device
        break
if arduino_port:
    ser = serial.Serial(arduino_port, 9600)
    while True:
        data = ser.readline().decode("utf-8").strip()
        print(data)
        # requests.post("http://localhost:5000/card_state", json={"state": data})
    
