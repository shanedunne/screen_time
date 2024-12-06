import json
from datetime import date, datetime, timedelta

# get activity log information. If log does not exist, return an empty dict
def get_activity_log():
    try:
        with open("./data/activity_log.json", 'r') as openfile:
            return json.load(openfile)
    except FileNotFoundError:
        return {}

# function to turn seconds into hours - minutes - seconds
def convertToHours(seconds):
    seconds = seconds % (24 * 3600)
    hour = seconds // 3600
    seconds %= 3600
    minutes = seconds // 60
    seconds %= 60
     
    return "%d:%02d:%02d" % (hour, minutes, seconds)
    
# handle data stored on network activity
def handle_network_data():
    data_source = get_activity_log()

    all_daily_stats = []

    # get last 7 dates to acquire data
    last_seven_dates = []
    for i in range(7):
        day = date.today() - timedelta(days=i)
        iso = day.isoformat()
        last_seven_dates.append(iso)

    # for each device, get daily statistics, depending on day
    for mac, dates in data_source.items():
        daily_stats = {
            "device": mac,
            "dates": {},
        }

        # for each of the last 7 days, sum up the session times and store daily times with corresponding dates
        for day in last_seven_dates:
            if day in dates:
                # get daily total

                daily_time = 0
                longest_session = 0
                for session in dates[day].values():
                    daily_time += session.get("session_length", 0)
                    if session.get("session_length", 0) > longest_session:
                        longest_session = session.get("session_length", 0)
                
                daily_stats["dates"][day] = {
                    "daily_time": convertToHours(daily_time),
                    "longest_session": convertToHours(longest_session)
                }


            else:
                daily_stats["dates"][day] = 0
        
        # add to all daily stats
        all_daily_stats.append(daily_stats)
    
    return all_daily_stats


           

