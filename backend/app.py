import time
from flask import Flask, jsonify, request
from flask_cors import CORS
import serial.tools.list_ports
import serial

# Flask App Setup
app = Flask(__name__)
CORS(app)  # Enable CORS for the Flask app

# API to fetch leaderboard
@app.route("/leaderboard", methods=["GET"])
def leaderboard():
    leaderboard_data = {
        "Leader Board": {
            "1": "John Doe",
            "2": "Jane Smith",
            "3": "Alice Johnson"
        },
        "Ads": {
            "1": "https://example.com/ad1.jpg",
            "2": "https://example.com/ad2.jpg",
            "3": "https://example.com/ad3.jpg"
        }
    }
    return jsonify(leaderboard_data)

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
            data = ser.readline().decode("utf-8").strip()
            if data == '1':
                return jsonify({"card_inserted": True})
            else:
                return jsonify({"card_inserted": False})
        except Exception as e:
            print(e)
    return jsonify({"status": "error", "message": "No Arduino connected."})

# API to process barcode
@app.route("/process_barcode", methods=["POST"])
def process_barcode():
    data = request.json
    barcode = data.get("barcode")
    if barcode:
        return jsonify({"status": "success", "message": f"Barcode {barcode} processed."})
    return jsonify({"status": "error", "message": "No barcode provided."})


if __name__ == "__main__":
    app.run(debug=True, port=5000)
