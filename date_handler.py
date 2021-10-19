from datetime import datetime


def get_string_date_by_timestamp(timestamp):
    timestamp = int(timestamp)
    dt_object = datetime.fromtimestamp(timestamp)
    date_time = dt_object.strftime("%m/%d/%Y, %H:%M")
    return date_time


def get_today_date_to_time_stamp():
    now = datetime.now()
    timestamp = datetime.timestamp(now)
    return int(timestamp)


def convert_timestamps_to_date(data):
    for dictionary in data:
        timestamp = dictionary["submission_time"]
        dictionary["submission_time"] = get_string_date_by_timestamp(timestamp)
    return data
