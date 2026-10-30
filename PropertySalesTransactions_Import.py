import os
import requests
from dotenv import load_dotenv
import pandas as pd

load_dotenv()

# Configure your CKAN instance
CKAN_URL = "https://data.wprdc.org/api/action/datastore_search_sql"
API_KEY = os.getenv("WPRDC_TOKEN")

headers = {
    "Authorization": API_KEY,
    "Content-Type": "application/json"
}

# The body parameter payload matches standard CKAN actions
payload = {
    "sql": """SELECT * FROM \"5bbe6c55-bce6-4edb-9d04-68edeb6bf7b1\" WHERE "SALEDATE" >= '2026-10-01'""",
}

response = requests.post(CKAN_URL, json=payload, headers=headers)

if response.status_code == 200:
    data = response.json()
    if data.get("success"):
        df = pd.DataFrame(data.get("result").get("records"))
else:
    print(f"Error: {response.status_code}")

