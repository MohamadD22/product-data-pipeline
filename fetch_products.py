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
    return result.get('values', [])

def fetch_aliexpress_products(keyword):
    url = f"https://www.aliexpress.com/wholesale?SearchText={keyword.strip()}"
    print(f"Fetching URL: {url}")
    driver = webdriver.Chrome()  # Make sure you have the ChromeDriver installed and available in your PATH
    driver.get(url)
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    driver.quit()
    products = []
    for item in soup.select('.JIIxO'):
        name = item.select_one('.JIIxO ._1OUGS ._2c4iS').text if item.select_one('.JIIxO ._1OUGS ._2c4iS') else 'No name'
        link = item.select_one('a').get('href')
        price = item.select_one('.JIIxO ._3R8Xy ._2YmoW ._3CnGk').text if item.select_one('.JIIxO ._3R8Xy ._2YmoW ._3CnGk') else 'No price'
        product = {
            'name': name,
            'link': link,
            'price': price,
            'website': 'AliExpress'
        }
        print(f"Product found: {product}")
        products.append(product)
    print(f"Total products fetched for '{keyword}': {len(products)}")
    return products

# Function to write product data to Google Sheets
def write_product_data(products):
    sheet = service.spreadsheets()
    values = [[p['name'], p['link'], p['price'], p['website']] for p in products]
    body = {'values': values}
    sheet.values().update(spreadsheetId=spreadsheet_id, range='Product Data!A1', valueInputOption='RAW', body=body).execute()
def fetch_aliexpress_products(keyword):
    url = f"https://www.aliexpress.com/wholesale?SearchText={keyword}"
    print(f"Fetching URL: {url}")  # Debugging line
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
        print(f"Product found: {product}")  # Debugging line
        products.append(product)
    print(f"Total products fetched for '{keyword}': {len(products)}")  # Debugging line
    return products


#Step 1: Define the Function to Fetch Videos

from googleapiclient.discovery import build

def fetch_youtube_videos(keyword):
    api_key = 'AIzaSyBEUj7YIBHUVFUpJxHiBwzWO6IhppYtb1A'  # Replace this with your actual YouTube API key
    youtube = build('youtube', 'v3', developerKey=api_key)
    request = youtube.search().list(q=keyword, part='snippet', maxResults=5)
    response = request.execute()
    videos = []
    for item in response['items']:
        video = {
            'title': item['snippet']['title'],
            'channel': item['snippet']['channelTitle'],
            'link': f"https://www.youtube.com/watch?v={item['id']['videoId']}",
            'description': item['snippet']['description'],
            'published_at': item['snippet']['publishedAt']
        }
        videos.append(video)
    return videos

# Step 2: Define the Function to Write Video Data to Google Sheets

def write_video_data(videos):
    sheet = service.spreadsheets()
    values = [[v['title'], v['channel'], v['link'], v['description'], v['published_at']] for v in videos]
    body = {'values': values}
    sheet.values().update(spreadsheetId=spreadsheet_id, range='Multimedia Content!A2', valueInputOption='RAW', body=body).execute()

# Step 3: Integrate These Functions into Your Main Script

if __name__ == '__main__':
    keywords = read_keywords()
    all_products = []
    all_videos = []
    for keyword in keywords:
        keyword = keyword[0]  # Extract keyword from the list
        print(f"Fetching products for keyword: {keyword}")  # Debugging line
        products = fetch_aliexpress_products(keyword)
        print(f"Products fetched: {products}")  # Debugging line
        all_products.extend(products)
        print(f"Fetching videos for keyword: {keyword}")  # Debugging line
        videos = fetch_youtube_videos(keyword)
        print(f"Videos fetched: {videos}")  # Debugging line
        all_videos.extend(videos)
    write_product_data(all_products)
    write_video_data(all_videos)
    print("Data retrieval completed.")
