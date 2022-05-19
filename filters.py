import os
import mimetypes
import arrow

def datetimeformat(date_str):
    dt = arrow.get(date_str, 'DD/MM/YYYY HH:mm:ss')
    return dt.humanize()

def datetimeformatBucket(date_str):
    dt = arrow.get(date_str)
    return dt.humanize()