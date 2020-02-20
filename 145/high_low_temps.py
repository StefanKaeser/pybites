from collections import namedtuple
from datetime import datetime
import urllib.request

import pandas as pd

DATA_FILE = "https://bites-data.s3.us-east-2.amazonaws.com/weather-ann-arbor.csv"
STATION = namedtuple("Station", "ID Date Value")

filename = "weather"
# urllib.request.urlretrieve(DATA_FILE, filename)

LENGTH_YEAR = 4


def high_low_record_breakers_for_2015():
    """Extract the high and low record breaking temperatures for 2015

    The expected value will be a tuple with the highest and lowest record
    breaking temperatures for 2015 as compared to the temperature data
    provided.

    NOTE:
    The date values should not have any timestamps, should be a
    datetime.date() object. The temperatures in the dataset are in tenths
    of degrees Celsius, so you must divide them by 10

    Possible way to tackle this challenge:

    1. Create a DataFrame from the DATA_FILE dataset.

    2. Manipulate the data to extract the following:
       * Extract highest temperatures for each day / station pair between 2005-2015
       * Extract lowest temperatures for each  day / station  between 2005-2015
       * Remove February 29th from the dataset to work with only 365 days

    3. Separate data into two separate DataFrames:
       * high/low temperatures between 2005-2014
       * high/low temperatures for 2015

    4. Iterate over the 2005-2014 data and compare to the 2015 data:
       * For any temperature that is higher/lower in 2015 extract ID,
         Date, Value
         
    5. From the record breakers in 2015, extract the high/low of all the
       temperatures
       * Return those as STATION namedtuples, (high_2015, low_2015)
    """
    df = pd.read_csv(filename)

    # Remove leap day February 29th
    df = df[~df["Date"].str.contains("02-29")]

    # Add identifier for day / station pair
    df["Station_Day"] = df["ID"] + df["Date"].str[LENGTH_YEAR:]

    # Split in pre 2015 and 2015
    df_pre_2015 = df[~df["Date"].str.contains("2015")]
    df_2015 = df[df["Date"].str.contains("2015")]

    # Extract the record highs and lows
    df_highs = (
        df_pre_2015[df_pre_2015["Element"] == "TMAX"][["Station_Day", "Data_Value"]]
        .groupby("Station_Day")
        .max()
    )
    df_lows = (
        df_pre_2015[df_pre_2015["Element"] == "TMIN"][["Station_Day", "Data_Value"]]
        .groupby("Station_Day")
        .min()
    )

    record_breakers = []
    for _, (station, day, element, value, station_day) in df_2015.iterrows():
        if element == "TMAX":
            record_high = int(df_highs.loc[station_day])
            broke_record = value > record_high
        elif element == "TMIN":
            record_low = int(df_lows.loc[station_day])
            broke_record = value < record_low

        if broke_record:
            record_breakers.append(
                STATION(station, datetime.strptime(day, "%Y-%m-%d").date(), value / 10)
            )

    record_breakers = sorted(record_breakers, key=lambda x: x[2])  
    return record_breakers[-1], record_breakers[0]

high_low_record_breakers_for_2015()
