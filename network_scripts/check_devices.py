import json
import subprocess
from datetime import date, datetime, timedelta
import uuid

# get mac and ip data to use in following functions
def get_data():
    with open("./data/mac_ip.json", 'r') as openfile:
        # assign data to variable
        json_object = json.load(openfile)
    return json_object

# get activity log information. If log does not exist, return an empty dict
def get_activity_log():
    try:
        with open("./data/activity_log.json", 'r') as openfile:
            return json.load(openfile)
    except FileNotFoundError:
        return {}

# write to the the json file with new activity
def save_activity_log(activity_log):
    with open("./data/activity_log.json", 'w') as openfile:
        json.dump(activity_log, openfile, indent=4)

def check_activity():
    mac_ip_addresses = get_data()
    for mac, ip in mac_ip_addresses.items():
        try:
            # Ping the IP address to check if it is active
            subprocess.check_output(f"ping -c 1 -W 1 {ip}", shell=True, stderr=subprocess.STDOUT)
            activity = "Online"
        except subprocess.CalledProcessError:
            activity = "Offline"
    
        # assign activity log to variable
        activity_log = get_activity_log()

        # get todays date
        today = date.today().isoformat()

        # get current time
        current_time = datetime.now().isoformat()

        # check if mac of device has been entered into the log before
        if mac not in activity_log:
            activity_log[mac] = {}

        # check if there has been a session today for the mac
        if today not in activity_log[mac]:
            activity_log[mac][today] = {}  
        
        # check if device status is active
        if activity == "Online":

            # check if any recorded sessions for today
            if not activity_log[mac][today]:
                session_id = str(uuid.uuid1())
                activity_log[mac][today][session_id] = {

                    # need to fix format
                    "start_time": current_time,
                    "last_time": current_time
                }
            else:
                # get the id of the last session
                last_session_id = list(activity_log[mac][today].keys())[-1]

                # get the last session using the id
                last_session = activity_log[mac][today][last_session_id]

                # get current and last time in a comparable format, not string
                formatted_current_time = datetime.fromisoformat(current_time)

                last_time = last_session["last_time"]
                formatted_last_time = datetime.fromisoformat(last_time)

                # if difference greater than 60 seconds, session has expired and create a new one
                if ((formatted_current_time - formatted_last_time) > timedelta(seconds=60)):
                    new_session_id = str(uuid.uuid1())
                    activity_log[mac][today][new_session_id] = {
                        "start_time": current_time,
                        "last_time": current_time
                    }
                # else, update last time
                else:
                    last_session["last_time"] = current_time
                
        else:
                # If offline, close the last session if it's still open
                if activity_log[mac][today]:
                    last_session_id = list(activity_log[mac][today].keys())[-1]
                    last_session = activity_log[mac][today][last_session_id]
                    if last_session["last_time"] is None:
                        last_session["last_time"] = current_time.isoformat()

        print(f"MAC Address: {mac}, IP Address: {ip}, Status: {activity}")

        # Save the updated activity log
        save_activity_log(activity_log)
