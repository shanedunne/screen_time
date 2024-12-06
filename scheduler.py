from flask import Flask, jsonify
from threading import Thread
import schedule
import time
from network_scripts import get_ip, check_devices, data_handler
import blynk_feed

app = Flask(__name__)

# create api route
@app.route("/api/devices/stats", methods=["GET"])
def get_device_stats():
    stats = data_handler.handle_network_data()
    return jsonify(stats)

def start_flask_app():
    app.run(debug=True, use_reloader=False, port=5001)

# set up threads to run api in background
flask_thread = Thread(target=start_flask_app)
flask_thread.daemon = True
flask_thread.start()

# schedule getting IP every 6 hours to ensure there is no changes
schedule.every(6).hours.do(get_ip.find_ip_for_mac)

# schedule the activity checker script to run every 15 seconds
schedule.every(15).seconds.do(check_devices.check_activity)

while True:
    schedule.run_pending()
    blynk_feed.run_blynk()
    time.sleep(1)