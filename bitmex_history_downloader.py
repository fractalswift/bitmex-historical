import requests
import pandas as pd
import numpy as np
import bitmex
from datetime import date, datetime, timedelta


resolution_from_time_diff = {

    60: '1m',
    300: '5m',
    3600: '1h',
    86400: '1d',

}

minutes_from_resolution = {

    '1m': 750,
    '5m': 3750,
    '1h': 45000,
    '1d': 1080000,

}


def make_base_sheet(coinpair, resolution, start_time, end_time):

    parameters = {"binSize": resolution, "partial": False, 'symbol': coinpair, 'count': 750, 'reverse': 'false', 'startTime': start_time, 'endTime': end_time}

    first_hour_of_minutes = requests.get("https://www.bitmex.com/api/v1/trade/bucketed", params=parameters)

    first_hour_df = pd.read_json(first_hour_of_minutes.content)

    return first_hour_df


def add_750_rows(base_sheet):

    # Work out the resolution automatically

    time_diff = base_sheet.at[3, 'timestamp'] - base_sheet.at[2, 'timestamp']

    seconds = round(time_diff.total_seconds())

    resolution = resolution_from_time_diff.get(seconds)

    # Work out the coinpair automatically

    coinpair = base_sheet.at[0, 'symbol']

    # Work out how many minutes ahead the next end date should be to make 750 rows at current resolution

    minutes_ahead = minutes_from_resolution.get(resolution)

    # Get the date from the bottom row so we know where to start asking for the next 750 rows

    last_date_index = (len(base_sheet) - 1)

    last_date = base_sheet.at[last_date_index, 'timestamp']

    next_end_date = last_date + pd.DateOffset(minutes=minutes_ahead)   # This must change depending on resolution

    start_time = (last_date + pd.DateOffset(minutes=1))

    end_time = next_end_date

    # Set the paramaters for the API call based on the things above

    parameters = {"binSize": resolution, "partial": False, 'symbol': coinpair, 'count': 750, 'reverse': 'false', 'startTime': start_time, 'endTime': end_time}

    next_750_rows = requests.get("https://www.bitmex.com/api/v1/trade/bucketed", params=parameters)

    next_750_rows_df = pd.read_json(next_750_rows.content)

    # Merge the rows with the base sheet

    updated_sheet = base_sheet.merge(next_750_rows_df, how='outer')

    return updated_sheet


def make_150_update_api_calls(base_sheet):

    base_sheet_updated = add_750_rows(base_sheet)

    for i in range(1, 148):

        try:

            base_sheet_updated = add_750_rows(base_sheet_updated)

        except Exception:
            print('Ran out of rows to update, we should be up to date ish now')
            break

    return base_sheet_updated
