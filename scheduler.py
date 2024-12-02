import schedule
import time
from network_scripts import get_ip, check_devices

# schedule getting IP every 6 hours to ensure there is no changes
schedule.every(6).hours.do(get_ip.find_ip_for_mac)

# schedule the activity checker script to run every 15 seconds
schedule.every(15).seconds.do(check_devices.check_activity)

while True:
    schedule.run_pending()
    time.sleep(1)