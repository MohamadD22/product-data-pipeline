import requests
from bs4 import BeautifulSoup
from googleapiclient.discovery import build
from google.oauth2 import service_account

SCOPES = ['https://www.googleapis.com/auth/spreadsheets']
SERVICE_ACCOUNT_FILE = 'credentials.json'

credentials = service_account.Credentials.from_service_account_file(
    SERVICE_ACCOUNT_FILE, scopes=SCOPES)

service = build('sheets', 'v4', credentials=credentials)
spreadsheet_id = '1VWvXG3nF0oQl-vpus4XiSQ798QMfwHFbnWw32ulIoD4'

# Function to read keywords from Google Sheets
def read_keywords():
    sheet = service.spreadsheets()
    result = sheet.values().get(spreadsheetId=spreadsheet_id, range='User Input!A:A').execute()
    keywords = result.get('values', [])
    print("Keywords read from sheet:", keywords)  # Debugging statement
    return keywords

# Function to fetch products from AliExpress
def fetch_aliexpress_products(keyword):
    url = f"https://www.aliexpress.com/wholesale?SearchText={keyword}"
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    products = []
    for item in soup.select('.item'):
        product = {
            'name': item.select_one('.product-title').text,
            'link': item.select_one('a').get('href'),
            'price': item.select_one('.price').text,
            'website': 'AliExpress'
        }
        products.append(product)
    print(f"Products fetched for {keyword}:", products)  # Debugging statement
    return products

# Function to write product data to Google Sheets
def write_product_data(products):
    sheet = service.spreadsheets()
    values = [[p['name'], p['link'], p['price'], p['website']] for p in products]
    body = {'values': values}
    result = sheet.values().update(spreadsheetId=spreadsheet_id, range='Product Data!A2', valueInputOption='RAW', body=body).execute()
    print("Data written to sheet:", result)  # Debugging statement
# Main function with debugging info (Note: It didn't work; the data didn't populate in google sheet as expected as I tried to solve this issue many times)
if __name__ == '__main__':
    keywords = read_keywords()
    all_products = []
    for keyword in keywords:
        keyword = keyword[0]  # Extract keyword from the list
        products = fetch_aliexpress_products(keyword)
        all_products.extend(products)
    write_product_data(all_products)
    print("Product data retrieval completed.")
