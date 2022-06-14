import os
import mimetypes
import arrow
# python file to create filters for formating dates and file types

# formats date in 'humanized' manner
def datetimeformat(date_str):
    dt = arrow.get(date_str, 'DD/MM/YYYY HH:mm:ss')
    return dt.humanize()

# formats date in 'humanized' manner
def datetimeformatBucket(date_str):
    dt = arrow.get(date_str)
    return dt.humanize()

# returns type of file
def file_type(key):
    file_info = os.path.splitext(key) 
    file_extension = file_info[1]
    try:
        return mimetypes.types_map[file_extension]
    except KeyError():
        return 'Unknown'
