import boto3
from botocore.exceptions import ClientError
import os
from dotenv import load_dotenv
import json
from network_scripts import data_handler

# Load environment variables from .env file
load_dotenv()

# Get AWS credentials from environment variables
AWS_ACCESS_KEY_ID = os.getenv('AWS_ACCESS_KEY_ID')
AWS_SECRET_ACCESS_KEY = os.getenv('AWS_SECRET_ACCESS_KEY')

def issue_all_user_emails():

    # get users from users.json
    try:
        with open("./data/users.json", 'r') as userfile:
            data = json.load(userfile)
    except FileNotFoundError:
        return {}
    
    users = data["users"]
    print(users)
    
    # for each user, assign required variables
    for user in users:
        firstName = user.get("firstName")
        email = user.get("email")
        id = user.get("_id")

        try:
            with open("./data/devices.json", 'r') as devicefile:
                deviceData = json.load(devicefile)
        except FileNotFoundError:
            return {}
        devices = deviceData["devices"]

        deviceStats = { "devices" : []}

        # for each device associated with user via id, get mac and device name
        for device in devices:
            if id == device.get("userid"):
                mac = device["mac"]
                deviceName = device["device"]
                print(f'mac: {mac}')

                # call function that gets past 7 day stats
                allStats = data_handler.handle_network_data()

                # if the users mac is in allStats, get the weekly time
                if mac in allStats:
                    mac_data = allStats[mac]["dates"]

                    weekly_time = sum(
                        entry.get("daily_time", 0) for entry in mac_data.values() if isinstance(entry, dict)
                        )

                    # append the device info to user specific devices
                    deviceStats["devices"].append({
                        "mac": mac,
                        "deviceName": deviceName,
                        "weekly_time": data_handler.convertToHours(weekly_time)

                    })

                
        # call email function with data for email
        summary_email = send_weekly_email(firstName, email, deviceStats)


        



def send_weekly_email(first_name, email, device_stats):
    # Replace sender@example.com with your "From" address.
    # This address must be verified with Amazon SES.
    SENDER = os.getenv('SENDER_EMAIL')

    # Replace recipient@example.com with a "To" address. If your account 
    # is still in the sandbox, this address must be verified.
    RECIPIENT = email

    # Specify a configuration set. If you do not want to use a configuration
    # set, comment the following variable, and the 
    # ConfigurationSetName=CONFIGURATION_SET argument below.
    # CONFIGURATION_SET = "ConfigSet"

    # If necessary, replace us-west-2 with the AWS Region you're using for Amazon SES.
    AWS_REGION = "eu-west-1"



    # The subject line for the email.
    SUBJECT = "Weekly Screen Time Recap"

    # The email body for recipients with non-HTML email clients.
    BODY_TEXT = f"Hello {first_name},\n\n"
    BODY_TEXT += "Here is your weekly usage summary for your devices:\n\n"
    for device in device_stats["devices"]:
        BODY_TEXT += f"Device: {device['deviceName']}\n"
        BODY_TEXT += f"  - Weekly Usage: {device['weekly_time']} hours\n\n"
                
   # Generate the email body (HTML version)
    BODY_HTML = f"""
    <html>
    <head></head>
    <body>
      <h1>Weekly Usage Summary for Your Devices</h1>
      <p>Hello {first_name},</p>
      <p>Here is your weekly usage summary for your devices:</p>
      <ul>
    """
    for device in device_stats["devices"]:
        BODY_HTML += f"""
        <li>
          <strong>Device:</strong> {device['deviceName']}<br>
          <strong>Weekly Usage:</strong> {device['weekly_time']} hours
        </li>
        """
    BODY_HTML += """
      </ul>
      <br>
      <p> Be sure to stop by <a href="http://localhost:4000/">Screen Time</a> for more information </p>
    </body>
    </html>
    """      

    # The character encoding for the email.
    CHARSET = "UTF-8"

    # Create a new SES resource and specify a region.
    client = boto3.client(
    'ses',
    region_name=AWS_REGION,
    aws_access_key_id=AWS_ACCESS_KEY_ID,
    aws_secret_access_key=AWS_SECRET_ACCESS_KEY
)



    # Try to send the email.
    try:
        #Provide the contents of the email.
        response = client.send_email(
            Destination={
                'ToAddresses': [
                    RECIPIENT,
                ],
            },
            Message={
                'Body': {
                    'Html': {
                        'Charset': CHARSET,
                        'Data': BODY_HTML,
                    },
                    'Text': {
                        'Charset': CHARSET,
                        'Data': BODY_TEXT,
                    },
                },
                'Subject': {
                    'Charset': CHARSET,
                    'Data': SUBJECT,
                },
            },
            Source=SENDER,
            # If you are not using a configuration set, comment or delete the
            # following line
            # ConfigurationSetName=CONFIGURATION_SET,
        )
    # Display an error if something goes wrong.	
    except ClientError as e:
        print(e.response['Error']['Message'])
    else:
        print("Email sent! Message ID:"),
        print(response['MessageId'])