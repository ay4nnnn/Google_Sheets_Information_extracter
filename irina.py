import os
print(os.getcwd())
print(os.path.exists('credentials.json'))




import os.path
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

# Read-only access to Google Sheets
SCOPES = ['https://www.googleapis.com/auth/spreadsheets']

SPREADSHEET_ID = 'YOUR_REAL_SPREADSHEET_ID'
RANGE_NAME = 'Sheet1!A1:E10'


def main():
    creds = None

    # Load saved credentials
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)

    # If credentials are missing or invalid, log in
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES
            )
            creds = flow.run_local_server(port=0)

        # Save credentials for next run
        with open('token.json', 'w') as token:
            token.write(creds.to_json())

    # Call the Sheets API
    service = build('sheets', 'v4', credentials=creds)
    sheet = service.spreadsheets()

    result = sheet.values().get(
        spreadsheetId=SPREADSHEET_ID,
        range=RANGE_NAME
    ).execute()

    values = result.get('values', [])

    if not values:
        print('No data found.')
    else:
        for row in values:
            print(row)


if __name__ == '__main__':
    main()