import datetime

def string_to_date(date_string):
    date_object = datetime.datetime.strptime(date_string, "%Y-%m-%d")
    return date_object.date()