import os
import requests
from dotenv import load_dotenv
import pandas as pd
from datetime import datetime
import matplotlib.pyplot as plt

load_dotenv()

# CKAN Variables
CKAN_URL = "https://data.wprdc.org/api/action/datastore_search_sql"
API_KEY = os.getenv("WPRDC_TOKEN")
RESOURCE_ID = '66cdcd57-6c92-4aaa-8800-0ed9d8f03e22'

# Date and Pagination
date_column = "census_date"
page_size = 20000
date_range_start = "2024-01-01"
date_range_end = "2026-10-30"

headers = {
    "Authorization": API_KEY,
    "Content-Type": "application/json"
}


# Helper functions
def is_valid_date(date_string, date_format="%Y-%m-%d"):
    try:
        datetime.strptime(date_string, date_format)
        return True
    except ValueError:
        return False


def month_ranges(month_start_date, month_end_date):
    if not is_valid_date(month_start_date):
        raise ValueError(f"Invalid date format in start date: {month_start_date}")
    if not is_valid_date(month_end_date):
        raise ValueError(f"Invalid date format in end date: {month_end_date}")

    # Generate month starts between boundaries
    month_starts = pd.date_range(start=month_start_date, end=month_end_date, freq="MS")

    # Construct the list of ranges
    ranges = []
    current_start = pd.to_datetime(month_start_date)

    for start in month_starts:
        if start > current_start:
            ranges.append((current_start.strftime("%Y-%m-%d"), (start - pd.Timedelta(days=1)).strftime("%Y-%m-%d")))
            current_start = start

    # Append the final remaining partial month
    ranges.append((current_start.strftime("%Y-%m-%d"), pd.to_datetime(month_end_date).strftime("%Y-%m-%d")))
    return ranges


def fetch_ckan_data_page(date_start, date_end, limit, offset):
    # Construct the SQL query with LIMIT and OFFSET for pagination
    sql_query = f"""SELECT * FROM "{RESOURCE_ID}" WHERE "{date_column}" >= '{date_start}' AND "{date_column}" <= '{date_end}' ORDER BY "_id" LIMIT {limit} OFFSET {offset}"""
    payload = {"sql": sql_query}
    response = requests.get(CKAN_URL, params=payload)
    response.raise_for_status()
    result = response.json()
    if result.get("success"):
        # datastore_search_sql returns records directly in the result object
        return result["result"]["records"]
    else:
        print(f"API Error: {result.get('error')}")
        return []


def get_all_records(record_start_date=None, record_end_date=None):
    all_records = []
    offset = 0
    while True:
        print(f"Fetching records {offset} to {offset + page_size}...")
        records = fetch_ckan_data_page(date_start=record_start_date, date_end=record_end_date, limit=page_size, offset=offset)
        if not records:
            break
        all_records.extend(records)
        if len(records) < page_size:
            break
        offset += page_size
    return all_records


# Extract data range
months_to_pull = month_ranges(date_range_start, date_range_end)
all_records_in_range = []
for month_interval in months_to_pull:
    print("Pulling daily census from " + month_interval[0] + " to " + month_interval[1])
    start_date = month_interval[0]
    end_date = month_interval[1]
    new_sets = get_all_records(record_start_date=month_interval[0], record_end_date=month_interval[1])
    print("adding new set")
    all_records_in_range.extend(new_sets)

print(str(len(all_records_in_range)) + " rows imported from WPRDC")
df = pd.DataFrame(all_records_in_range)
df['census_date'] = pd.to_datetime(df['census_date'])
df['Month'] = df['census_date'].dt.to_period('M')
race_code = {
    "A": "Asian or Pacific Islander",
    "B": "Black or African American",
    "H": "Hispanic",
    "I": "American Indian or Alaskan Native",
    "U": "Unknown",
    "W": "White",
    "x": "Biracial",
    "O": "All Others"
}
df['race'] = df['race'].map(race_code)
df['years_incarcerated'] = df['age_at_census'] - df['age_at_booking']
filtered_df = df[(df['age_at_census'] < 125) & (df['age_at_census'] > 10)]

pivot_df = filtered_df.pivot_table(
    values='age_at_census',
    index='race',
    columns='Month',
    aggfunc='mean'
)

pivot_long = pivot_df.T
pivot_long = pivot_long.reset_index()

pivot_df_inc = filtered_df.pivot_table(
    values='years_incarcerated',
    index='race',
    columns='Month',
    aggfunc='mean'
)

pivot_long_inc = pivot_df_inc.T
pivot_long_inc = pivot_long_inc.reset_index()

# Plotting
ax = pivot_long.plot(x='Month', y='White', label='White Avg. Age (Left Axis)', color='blue')
pivot_long_inc.plot(x='Month', y='White', label='White Avg. Years Incarcerated (Right Axis)', color='purple', secondary_y=True, ax=ax)
ax2 = pivot_long.plot(x='Month', y='Black or African American', label='Black Avg. Age (Left Axis)', color='red', ax=ax)
pivot_long_inc.plot(x='Month', y='Black or African American', label='Black Avg. Years Incarcerated (Right Axis)', color='orange', secondary_y=True, ax=ax2)

