import time
from flask import Flask, jsonify, request
from flask_cors import CORS
import serial.tools.list_ports
import serial

# Flask App Setup
app = Flask(__name__)
CORS(app)  # Enable CORS for the Flask app

@app.route("/cardstate", methods=["GET"])
def cardstate():
    ports = serial.tools.list_ports.comports()
    arduino_port = None

    for port in ports:
        if "USB" in port.description:
            arduino_port = port.device
            break
    if arduino_port:
        try:
            ser = serial.Serial(arduino_port, 9600)
            data = ser.readline().decode("utf-8", errors='ignore').strip()
            ser.close()
            if data == '1':
                return jsonify({"card_inserted": True})
            else:
                return jsonify({"card_inserted": False})
        except Exception as e:
            print(e)
    return jsonify({"status": "error", "message": "No Arduino connected."})

if __name__ == "__main__":
    app.run(debug=True, port=5000)
