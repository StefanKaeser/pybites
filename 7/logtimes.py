from datetime import datetime
import os
import urllib.request

SHUTDOWN_EVENT = "Shutdown initiated"

# prep: read in the logfile
logfile = os.path.join(os.getcwd(), "log")
urllib.request.urlretrieve(
    "https://bites-data.s3.us-east-2.amazonaws.com/messages.log", logfile
)

with open(logfile) as f:
    loglines = f.readlines()


def convert_to_datetime(line):
    """TODO 1:
       Extract timestamp from logline and convert it to a datetime object.
       For example calling the function with:
       INFO 2014-07-03T23:27:51 supybot Shutdown complete.
       returns:
       datetime(2014, 7, 3, 23, 27, 51)
    """
    date_str = line.split()[1]
    date = datetime.strptime(date_str, "%Y-%m-%dT%H:%M:%S")
    return date


def time_between_shutdowns(loglines):
    """TODO 2:
       Extract shutdown events ("Shutdown initiated") from loglines and
       calculate the timedelta between the first and last one.
       Return this datetime.timedelta object.
    """
    shutdown_loglines = [logline for logline in loglines if SHUTDOWN_EVENT in logline]
    shutdown_dts = [convert_to_datetime(logline) for logline in shutdown_loglines]
    return shutdown_dts[1] - shutdown_dts[0]
