import json
from datetime import date, datetime, timedelta


# get activity log information. If log does not exist, return an empty dict
def get_activity_log():
    try:
        with open("./data/activity_log.json", 'r') as openfile:
            return json.load(openfile)
    except FileNotFoundError:
        return {}
    
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
            "dates": {}
        }

        # for each of the last 7 days, sum up the session times and store daily times with corresponding dates
        for day in last_seven_dates:
            if day in dates:
                daily_time = sum(session.get("session_length", 0) for session in dates[day].values())
                daily_stats["dates"][day] = daily_time
            else:
                daily_stats["dates"][day] = 0
        
        # add to all daily stats
        all_daily_stats.append(daily_stats)
    
    return all_daily_stats

if __name__ == "__main__":
    daily_stats = handle_network_data()

    # Print the results for debugging
    for device_stats in daily_stats:
        print(f"Device: {device_stats['device']}")
        for date, time in device_stats["dates"].items():
            print(f"  Date: {date}, Daily Time: {time} seconds")