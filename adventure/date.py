from datetime import datetime

from dateutil.tz import tzutc, tzlocal


def now():
    """Return the current time UTC"""
    return datetime.now(tzutc())

