from flask import Flask, jsonify, request
from flask_cors import CORS
from threading import Thread
import schedule
import time
from network_scripts import get_ip, check_devices, data_handler, weekly_update_email
import blynk_feed
import json

app = Flask(__name__)
CORS(app)

# create api route
@app.route("/api/devices/stats", methods=["GET"])
def get_device_stats():
    stats = data_handler.handle_network_data()
    return jsonify(stats)

@app.route("/api/devices/newDevice", methods=["POST"])
def get_new_device():

    # gt new device from api
    device = request.json
    
    # open devices json file
    with open("./data/devices.json", 'r') as file:
        devices = json.load(file)

    # append device to devices
    devices["devices"].append(device)
    with open("./data/devices.json", 'w') as file:
        json.dump(devices, file, indent=4)
    
    # call the find ip function to seatch the network for the provided macs ip address
    updated_devices = get_ip.find_ip_for_mac()

    return jsonify({"message": "Device added successfully", "devices: ": updated_devices}), 200

def start_flask_app():
    app.run(debug=True, use_reloader=False, host="0.0.0.0", port=5001)

# set up threads to run api in background
flask_thread = Thread(target=start_flask_app)
flask_thread.daemon = True
flask_thread.start()

# schedule getting IP every 6 hours to ensure there is no changes
schedule.every(6).hours.do(get_ip.find_ip_for_mac)

# schedule the activity checker script to run every 15 seconds
schedule.every(15).seconds.do(check_devices.check_activity)

send_email = weekly_update_email.send_weekly_email()

while True:
    schedule.run_pending()
    blynk_feed.run_blynk()
    time.sleep(1)