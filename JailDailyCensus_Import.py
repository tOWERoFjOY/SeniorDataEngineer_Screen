import os
import requests
from dotenv import load_dotenv
import pandas as pd
from datetime import datetime

load_dotenv()

# Configure your CKAN instance
CKAN_URL = "https://data.wprdc.org/api/action/datastore_search_sql"
API_KEY = os.getenv("WPRDC_TOKEN")
RESOURCE_ID = '66cdcd57-6c92-4aaa-8800-0ed9d8f03e22'
date_column = "census_date"
page_size = 15000

headers = {
    "Authorization": API_KEY,
    "Content-Type": "application/json"
}


def is_valid_date(date_string, date_format="%Y-%m-%d"):
    try:
        datetime.strptime(date_string, date_format)
        return True
    except ValueError:
        return False


def month_ranges(start_date, end_date):
    if not is_valid_date(start_date):
        raise ValueError(f"Invalid date format in start date: {start_date}")
    if not is_valid_date(end_date):
        raise ValueError(f"Invalid date format in end date: {end_date}")

    # Generate month starts between boundaries
    month_starts = pd.date_range(start=start_date, end=end_date, freq="MS")

    # Construct the list of ranges
    ranges = []
    current_start = pd.to_datetime(start_date)

    for start in month_starts:
        if start > current_start:
            ranges.append((current_start.strftime("%Y-%m-%d"), (start - pd.Timedelta(days=1)).strftime("%Y-%m-%d")))
            current_start = start

    # Append the final remaining partial month
    ranges.append((current_start.strftime("%Y-%m-%d"), pd.to_datetime(end_date).strftime("%Y-%m-%d")))
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


def get_all_records(start_date=None, end_date=None):
    all_records = []
    offset = 0
    while True:
        print(f"Fetching records {offset} to {offset + page_size}...")
        records = fetch_ckan_data_page(date_start=start_date, date_end=end_date, limit=page_size, offset=offset)
        if not records:
            break
        all_records.extend(records)
        if len(records) < page_size:
            break
        offset += page_size
    return all_records


months_to_pull = month_ranges("2025-01-01", "2025-02-28")
all_records_in_range = []
for month_interval in months_to_pull:
    new_sets = get_all_records(start_date=month_interval[0], end_date=month_interval[1])
    print("adding new set")
    all_records_in_range.extend(new_sets)

df = pd.DataFrame(all_records_in_range)
