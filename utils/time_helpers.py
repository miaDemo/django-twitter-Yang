from datetime import datetime
import pytz # python time zone

def utc_now():
    return datetime.now.replace(tzinfo=pytz.utc)