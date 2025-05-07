# pages/google_sheet.py
import requests
from data.config import SHEETY_ENDPOINT, INITIAL_SHEET_NAMES

class GoogleSheet:
    def __init__(self):
        self.base_endpoint = SHEETY_ENDPOINT
        self.sheet_names = INITIAL_SHEET_NAMES

    def get_users(self):
        endpoint = f"{self.base_endpoint}users"
        print(f"Fetching users from: {endpoint}")
        response = requests.get(endpoint)
        print(f"Response status code: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            return data['users']
        else:
            raise Exception(f"Failed to retrieve users. Status code: {response.status_code}")

    def get_destinations(self, sheet_name):
        # Convert sheet_name to lowercase
        sheet_name = sheet_name.lower()
        endpoint = f"{self.base_endpoint}{sheet_name}"
        print(f"Fetching destinations from: {endpoint}")
        response = requests.get(endpoint)
        print(f"Response status code: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            return data[sheet_name]
        else:
            raise Exception(f"Failed to retrieve destinations for sheet {sheet_name}. Status code: {response.status_code}")

    def update_row(self, sheet_name, row_id, new_data):
        try:
            endpoint = f"{self.base_endpoint}{sheet_name}/{row_id}"
            data = {sheet_name: new_data}
            print(f"Attempting to update row {row_id} in sheet '{sheet_name}'")
            print(f"Update endpoint: {endpoint}")
            print(f"Update data: {data}")
            response = requests.put(endpoint, json=data)
            print(f"Update response status: {response.status_code}")
            print(f"Update response content: {response.text}")
            return response.status_code == 200
        except Exception as e:
            print(f"Error updating row: {str(e)}")
            return False

    def create_column(self, sheet_name, column_name, default_value=""):
        endpoint = f"{self.base_endpoint}{sheet_name}"
        data = {sheet_name: {column_name: default_value}}
        response = requests.post(endpoint, json=data)
        return response.status_code == 200

    def add_missing_columns(self, sheet_name):
        missing_columns = {
            "flightDate": "",
            "dateFound": "",
            "timesUpdated": 0
        }
        for column, default_value in missing_columns.items():
            self.create_column(sheet_name, column, default_value)