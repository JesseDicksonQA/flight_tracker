import requests
from data.config import KIWI_API_ENDPOINT, KIWI_API_KEY


class FlightAPI:
    def __init__(self):
        self.api_key = KIWI_API_KEY
        self.endpoint = KIWI_API_ENDPOINT

    def search_flights(self, origin, destinations, date_from, date_to):
        headers = {
            "apikey": self.api_key
        }
        params = {
            "fly_from": origin,
            "fly_to": ",".join(destinations),
            "date_from": date_from.strftime("%d/%m/%Y"),
            "date_to": date_to.strftime("%d/%m/%Y"),
            "curr": "USD",
            "sort": "price",
            "limit": 10,  # Number of results per query
            "max_stopovers": 1,  # Maximum number of stopovers
            "vehicle_type": "aircraft",
            "partner_market": "us",
            "locale": "en",
            # "one_for_city": 1,  # Returns only one result per city pair (0 = no, 1 = yes)
            "adults": 1,
            "children": 0,
            "selected_cabins": "M",  # Cabin options: M (economy), W (economy premium), C (business), F (first class)
            # "adult_hold_bag": "1",  # Number of checked bags
            # "adult_hand_bag": "1",  # Number of carry-on bags
            # Additional parameters you might want to use:
            # "price_from": 10,           # Minimum price
            # "price_to": 500,            # Maximum price
            # "dtime_from": "00:00",      # Departure time from
            # "dtime_to": "23:59",        # Departure time to
            # "atime_from": "00:00",      # Arrival time from
            # "atime_to": "23:59",        # Arrival time to
            # "ret_from_diff_airport": 0, # Return from different airport (0 = no, 1 = yes)
            # "ret_to_diff_airport": 0,   # Return to different airport (0 = no, 1 = yes)
            # "max_fly_duration": 20,     # Maximum flight duration in hours
            "flight_type": "oneway",  # Flight type: round, oneway "oneway"
            # "one_per_date": 0,          # Only one flight per date (0 = no, 1 = yes)
            # "only_working_days": False, # Search only for working days
            # "only_weekends": False,     # Search only for weekends
            # "partner_market": "us",     # Country code for partner market (e.g., "us" for United States)
            # "max_fly_duration": 60,     # Maximum flight duration in hours

        }

        print(f"Searching flights with params: {params}")
        print(f"API Endpoint: {self.endpoint}/search")
        print(f"API Key (first 5 chars): {self.api_key[:5]}...")
        try:
            response = requests.get(f"{self.endpoint}/search", headers=headers, params=params)
            print(f"Flight search response status: {response.status_code}")

            if response.status_code == 200:
                data = response.json()
                print(f"Received {len(data.get('data', []))} flight results")

                # Separate Spirit and non-Spirit flights
                non_spirit_flights = [f for f in data.get('data', []) if f['airlines'][0] != 'NK']
                spirit_flights = [f for f in data.get('data', []) if f['airlines'][0] == 'NK']

                # Sort both lists by price
                non_spirit_flights.sort(key=lambda x: x['price'])
                spirit_flights.sort(key=lambda x: x['price'])

                # Prepare the result
                result = data.copy()
                result['data'] = non_spirit_flights  # Set non-Spirit flights as main data
                if spirit_flights:
                    result['spirit_flight'] = spirit_flights[0]  # Add cheapest Spirit flight if available

                return result
            else:
                print(f"Error in flight search: {response.text}")
                return {"data": [], "spirit_flight": None}
        except Exception as e:
            print(f"Exception in flight search: {str(e)}")
            return {"data": [], "spirit_flight": None}