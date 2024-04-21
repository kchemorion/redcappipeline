import os
import pandas as pd
import requests
from urllib.parse import urlencode

def upload_data_to_redcap(api_url, api_key, data):
    """Send data to REDCap via the API."""
    fields = {
        'token': api_key,
        'content': 'record',
        'format': 'csv',
        'type': 'flat',
        'data': data,
        'overwriteBehavior': 'normal',
        'returnContent': 'count',
        'returnFormat': 'json'
    }
    response = requests.post(api_url, data=fields)
    return response.json()

def process_csv_files(directory, api_url, api_key):
    """Process each CSV file in the directory and upload it to REDCap."""
    for filename in os.listdir(directory):
        if filename.endswith('.csv'):
            file_path = os.path.join(directory, filename)
            try:
                df = pd.read_csv(file_path)
                # Convert DataFrame to CSV string format
                csv_data = df.to_csv(index=False)
                result = upload_data_to_redcap(api_url, api_key, csv_data)
                print(f"Uploaded {filename}: {result}")
            except Exception as e:
                print(f"Failed to process {filename}: {e}")

# Parameters
API_URL = 'https://your_redcap_instance/api/'
API_KEY = 'YOUR_API_KEY_HERE'  # Replace with your actual REDCap API key
CSV_DIRECTORY = '/path/to/your/csv/files'  # Path to the directory containing your CSV files

process_csv_files(CSV_DIRECTORY, API_URL, API_KEY)
