from google.oauth2 import service_account
from googleapiclient.discovery import build

SCOPES = ['https://www.googleapis.com/auth/spreadsheets']
SERVICE_ACCOUNT_FILE = 'credentials.json'

credentials = service_account.Credentials.from_service_account_file(
    SERVICE_ACCOUNT_FILE, scopes=SCOPES)

service = build('sheets', 'v4', credentials=credentials)
spreadsheet_id = '1VWvXG3nF0oQl-vpus4XiSQ798QMfwHFbnWw32ulIoD4'

# Function to read data from a sheet
def read_sheet(sheet_range):
    sheet = service.spreadsheets()
    result = sheet.values().get(spreadsheetId=spreadsheet_id, range=sheet_range).execute()
    return result.get('values', [])

# Example usage
if __name__ == '__main__':
    data = read_sheet('User Input!A:A')
    print(data)
