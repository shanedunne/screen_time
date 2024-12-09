import BlynkLib
import time
import os
from dotenv import load_dotenv
from sense_hat import SenseHat
from time import sleep

# Load environment variables
load_dotenv()

# create instance of SenseHat
sense = SenseHat()

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


# Initialise button as off
button_value = "0"

# handle messages to sensehat, triggered in blynk
@blynk.on("V2")
def longSessionWaring(value): 
    message = "Turn it off"
    button_value = value[0]

    # if switch is turned on, pass message to sensehat
    if button_value == "1":
        sense.show_message(message, text_colour=(255, 0, 0), scroll_speed=0.1)
    sleep(10)
    sense.clear()
    button_value = "0"
    blynk.virtual_write(2, button_value)
