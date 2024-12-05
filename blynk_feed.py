import BlynkLib
import time
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Blynk authentication token
BLYNK_AUTH = os.getenv('BLYNK_AUTH_CODE')
# Initialise the Blynk instance
blynk = BlynkLib.Blynk(BLYNK_AUTH)

# set function to run blynk. This will be called by the scheduler
def run_blynk():
        blynk.run()

# function to write to blynk with current session times
def current_session(mac, session_length):

    # format session length to minutes
    formatted_session_length = round(session_length/60)

    # if mac is xbox, write to xbox virtual pin
    if (mac == os.getenv('XBOX_MAC')):
        blynk.virtual_write(0, formatted_session_length)

        # log activated event
        blynk.log_event("xbox_active")

        # 60 minute session event
        if (formatted_session_length == 1):
             blynk.log_event("xbox_60_min")
    
    # if mac is tv, write to xbox virtual pin
    if (mac == os.getenv('TV_MAC')):
        blynk.virtual_write(1, formatted_session_length)

        # log activated event
        blynk.log_event("tv_active")

        # 90 minute session event
        if (formatted_session_length == 1):
             blynk.log_event("tv_90_min")
