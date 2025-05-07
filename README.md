# CATCH FLIGHTS

## Project Goals
- Fetch flight prices from Kiwi Flight API for destinations listed in a Google Sheet
- Update the Google Sheet with the lowest prices found
- Send email notifications when cheaper flights are found
- Run daily at 5:30 AM

## Configuration
- Google Sheet name: Flight Deals
- Columns: City (A), IATA Code (B), Lowest Price (C), Flight Date (D), Date Found (E), Times Updated (F)
- Each sheet represents a different home location

## APIs Used
- Kiwi Flight API
- Google Sheets API (via Sheety)

## Email Notifications
Notifications will be sent to jdicksonqa@gmail.com

## Folder Structure
catch_flights/
│
├── data/
│   └── config.py
├── pages/
│   ├── __init__.py
│   ├── google_sheet.py
│   └── flight_api.py
├── utils/
│   ├── __init__.py
│   └── email_sender.py
├── main.py
├── requirements.txt
└── README.md

## Features

- Fetches destination data from a Google Sheet
- Searches for flights using the Kiwi API
- Compares prices with previously recorded lowest prices
- Sends email alerts for new low prices
- Includes detailed flight information in the email:
  - Origin and destination cities and airports
  - Flight date and time
  - Airline
  - Price
  - Direct booking link

## Setup

1. Clone the repository
2. Install required packages: `pip install -r requirements.txt`
3. Set up your Google Sheet with the following columns:
   - city: Destination city
   - iataCode: IATA code(s) for the destination airport(s)
   - lowestPrice: Lowest price found (will be updated automatically)
4. Rename `config.template.py` to `config.py` in the `data` folder and update it with your own values:
   - SHEETY_ENDPOINT: Your Sheety API endpoint
   - KIWI_API_ENDPOINT: Kiwi API endpoint
   - KIWI_API_KEY: Your Kiwi API key
   - GMAIL_ADDRESS: Email address to send alerts from
   - GMAIL_PASSWORD: App password for the sender email
   - NOTIFICATION_EMAIL: Email address to receive alerts
   - INITIAL_SHEET_NAMES: List of sheet names in your Google Sheet

   **Note:** The `config.py` file is included in `.gitignore` to prevent exposing sensitive information.

## Usage

Run the script with: `python main.py`

The script will:
1. Fetch destinations from the Google Sheet
2. Search for flights to each destination
3. Compare prices with the lowest recorded price
4. Update the Google Sheet if a new low price is found
5. Send an email alert with detailed flight information
