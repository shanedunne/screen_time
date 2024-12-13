# Screen Time

Screen Time is an IoT project that uses a Raspberry Pi to detect known device activity and report it to the user. Consider it Apple's screen time weekly summary, for all the other devices in your life.

## Description

Screen Time, runs on a Raspbery Pi and uses commands executed via Python to allow users to track the activity of their devices. This works particularly well for those devices that are turned off when not in use, such as smart TVs and gaming consoles. The dashboard allows a user to create an account and add devices using device MAC addresses and nicknames. In the backend, if the added device is running on the same network as the Raspberry Pi, the python script will locate and store the device IP address, and ping it every 15 seconds. Data is recorded and viewable on the device specific page, navigated to from the dashboard. Weekly summary emails are also sent to the users, with stats on their device usage.

Blynk has also been integrated to show two directional data transmission, allowing the user to view current device session times, if a device is active and also trigger a message to the Raspberry Pi SenseHat, should someone be using a device for too long. 

## Getting Started

### Prerequisites 

* Raspberry Pi >= 4
* RPi SenseHat
* Python
* Node JS
* Blynk account

### Installing
The repo needs to be cloned to the RPI using the following command
```
https://github.com/shanedunne/screen_time.git

# cd into the directory

cd screen_time

```
The user then needs to install dependancies
```
# node
npm install 

# python
pip install -r requirements.txt -t .

# depending on your RPi OS, you may have issues with privelages installing python modules
# use the below to bypass restrictions - Note, this should be done with caution
pip install module_name --break-system-packages
```
#### Some integration requirements
* [Blynk](https://blynk.io/) - Create an account for integrating datastreams
* [AWS AES](https://aws.amazon.com/ses/) - Used to automate the weekly email summary
```
# Auth code for Blynk access
BLYNK_AUTH_CODE

# Blynk template ID
BLYNK_TEMPLATE_ID

# Amazon AWS Access Key
AWS_ACCESS_KEY_ID

# Amazon AWS Secret Access Key
AWS_SECRET_ACCESS_KEY

# Email to send weekly summary from. Must be verified on AWS SES
SENDER_EMAIL

# TV mac hard coded for Blynk integration purposes only
TV_MAC

# Xbox mac hard coded for Blynk integration purposes only
XBOX_MAC
```

#### Blynk Datastreams
For Blynk integration testing purposes, follow the below instructions. Variation in the below will require code changes
* Set up a template by connecting your RPi
* Create 3 datasteams and corresponding dashboard widgets
    * Datastream 0 - Type: Integer, Min: 0, Max: 600, Title: "XBOX_MAC", Dashboard: Display
    * Datastream 1 - Type: Integer, Min: 0, Max: 600, Title: "TV_MAC", Dashboard: Display
    * Datastream 2 - Type: Interger Min: 0, Max: 1, Default: 0, Title: RPi SenseHat Message. Dashboard: Switch
        * This switch will activate a message printed on the RPi SH LED



### Executing program
In order to run the program, open two bash terminals, navigate to the screen_time directory and enter the following commands, one per terminal
```
# run js system
node server.js

# run python backend
python scheduler.py

```

The dashboard will be viewable [here](http://localhost:4000/), hosted locally for now as RPi required on local network to give site any functionality

## Application Usage and Features
### Using the dashboard
Things you can do on the dashboard
* Sign Up for an account.
* Add a device with its MAC address and nicname
    * There is a link to help users find MAC addresses for different device types
* View the device page to see a 7 day usage chart
* Delete unwanted devices or devices entered with errors in MAC or nickname

### Backend execution and features
* The system works by retrieving MAC addresses provided in the frontend, storing them and locating their associated IP addresses
    * To handle dynamic IP addresses, the IP address finding script is scheduled to run every 6 hours, updating all device IP addresses
* Every 15 seconds, a ping is sent to see if the device is active
* If active, a session start time is logged, and a last_active time is logged for the most recent detection
* If the most recent detection is longer than 60 seconds, the application will assume a new session has been started, and will end the previous session and start recording activity again
* Data is fed to the dashboard via an API
* Every Monday morning, automated emails will be issued to users with their weekly statistics for devices assigned to their account


## Technologies used

- Javascript - for rendering data and components
- Python - running back end of application
- Handlebars - as the HTML templating system to produce the pages
- Bulma - CSS Framework
- Express JS - As the server
- Axios - for fetching data from external APIs
