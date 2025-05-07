# main.py
import json
from datetime import datetime, timedelta
from pages.google_sheet import GoogleSheet
from pages.flight_api import FlightAPI
from utils.email_sender import send_email , test_email_sending
import traceback


def is_budget_airline(flight):
    airlines = flight.get('airlines', [])
    return 'NK' in airlines or 'Spirit' in airlines or 'F9' in airlines or 'Frontier' in airlines

def check_flights():
    google_sheet = GoogleSheet()
    flight_api = FlightAPI()

    try:
        users = google_sheet.get_users()
        print(f"Retrieved {len(users)} users")

        for user in users:
            print(f"\nProcessing user: {user['user']}")
            origin = user['homeLocation']
            email = user['email']
            sheet_name = origin.lower()
            print(f"Sheet name for update: {sheet_name}")

            try:
                destinations = google_sheet.get_destinations(sheet_name)
                print(f"Retrieved {len(destinations)} destinations for {sheet_name}")

                for destination in destinations:
                    print(f"\nChecking flights for: {destination['city']}")
                    city = destination.get('city', '')
                    iata_codes = [code.strip() for code in destination.get('iataCode', '').split(',') if code.strip()]

                    if not iata_codes:
                        print(f"Skipping destination {city} due to missing IATA code.")
                        continue

                    lowest_price = destination.get('lowestPrice', '')
                    date_found = destination.get('dateFound', '')

                    if not lowest_price or (
                            date_found and datetime.now() - datetime.strptime(date_found, "%Y-%m-%d") > timedelta(
                            weeks=3)):
                        update_data = {
                            "lowestPrice": "",
                            "dateFound": "",
                            "timesUpdated": 0
                        }

                        print(f"Updating row for {destination['city']} in sheet {sheet_name}")
                        print(f"Attempting to update sheet: {sheet_name}")
                        print(f"Row ID: {destination['id']}, Update data: {update_data}")
                        update_result = google_sheet.update_row(sheet_name, destination['id'], update_data)
                        print(f"Update result: {update_result}")
                        lowest_price = float('inf')

                    else:
                        lowest_price = float(lowest_price)

                    print(f"Searching flights from {origin} to {', '.join(iata_codes)}")
                    date_from = datetime.now() + timedelta(days=1)
                    date_to = date_from + timedelta(days=180)
                    print(f"Searching flights from {origin} to {', '.join(iata_codes)}")
                    print(f"Date range: {date_from.strftime('%d/%m/%Y')} to {date_to.strftime('%d/%m/%Y')}")


                    flight_data = flight_api.search_flights(origin, iata_codes, date_from, date_to)

                    if 'data' in flight_data and flight_data['data']:
                        all_flights = flight_data['data']

                        # Separate budget and non-budget flights
                        budget_flights = [f for f in all_flights if is_budget_airline(f)]
                        non_budget_flights = [f for f in all_flights if not is_budget_airline(f)]

                        cheapest_flight = non_budget_flights[0] if non_budget_flights else None
                        budget_flight = budget_flights[0] if budget_flights else None

                        if cheapest_flight:
                            new_price = cheapest_flight['price']
                            print(f"Found non-budget flight: {origin} to {city} for ${new_price}")
                        else:
                            print(f"No non-budget flights found for {origin} to {city}")

                        if budget_flight:
                            budget_price = budget_flight['price']
                            print(f"Found budget airline flight: {origin} to {city} for ${budget_price}")
                        else:
                            budget_price = None
                            print(f"No budget airline flights found for {origin} to {city}")

                        if cheapest_flight and (
                                new_price < lowest_price or (budget_price and budget_price < lowest_price)):
                            print(f"New low price found for {city}!")
                            update_data = {
                                "lowestPrice": min(new_price, budget_price) if budget_price else new_price,
                                "dateFound": datetime.now().strftime("%Y-%m-%d"),
                                "flightDate": cheapest_flight.get('local_departure', '').split('T')[0],
                                "timesUpdated": destination.get('timesUpdated', 0) + 1
                            }

                            print(f"Updating row for {destination['city']} in sheet {sheet_name}")
                            update_result = google_sheet.update_row(sheet_name, destination['id'], update_data)
                            print(f"Update result: {update_result}")

                            subject = f"New Low Price Alert for {city}!"
                            body = f"Low price alert! Only ${min(new_price, budget_price) if budget_price else new_price} to fly from {origin} to {city}.\n\n"

                            if cheapest_flight:
                                body += f"Best non-budget flight:\n"
                                body += f"Price: ${new_price}\n"
                                body += f"Airlines: {', '.join(cheapest_flight.get('airlines', ['N/A']))}\n"
                                body += f"Flight Number: {cheapest_flight.get('flight_no', 'N/A')}\n"
                                body += f"Flight date: {update_data['flightDate']}\n"
                                body += f"Departure: {cheapest_flight.get('local_departure', 'N/A')}\n"
                                body += f"Arrival: {cheapest_flight.get('local_arrival', 'N/A')}\n"
                                body += f"Book here: {cheapest_flight.get('deep_link', 'N/A')}\n\n"

                            if budget_flight:
                                body += f"Budget airline option:\n"
                                body += f"Price: ${budget_price}\n"
                                body += f"Airlines: {', '.join(budget_flight.get('airlines', ['N/A']))}\n"
                                body += f"Flight Number: {budget_flight.get('flight_no', 'N/A')}\n"
                                body += f"Flight date: {budget_flight.get('local_departure', '').split('T')[0]}\n"
                                body += f"Departure: {budget_flight.get('local_departure', 'N/A')}\n"
                                body += f"Arrival: {budget_flight.get('local_arrival', 'N/A')}\n"
                                body += f"Book here: {budget_flight.get('deep_link', 'N/A')}\n"

                            print(f"Sending email to {email}")
                            send_email(email, subject, body)
                            print(f"Email sending result: {email}")
                        else:
                            print(f"No new low price found for {city}.")
                    else:
                        print(f"No flights found for {city}.")

            except Exception as e:
                print(f"Error processing destinations for {sheet_name}: {str(e)}")
                traceback.print_exc()

    except Exception as e:
        print(f"An error occurred: {str(e)}")
        traceback.print_exc()


if __name__ == "__main__":
    print("Starting flight check...")
    check_flights()
    print("Flight check finished. Exiting program.")