

from googleapiclient.discovery import build

# Define the Function to Fetch Videos
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

# Define the Function to Write Video Data to Google Sheets

def write_video_data(videos):
    sheet = service.spreadsheets()
    values = [[v['title'], v['channel'], v['link'], v['description'], v['published_at']] for v in videos]
    body = {'values': values}
    sheet.values().update(spreadsheetId=spreadsheet_id, range='Multimedia Content!A2', valueInputOption='RAW', body=body).execute()

# Integrate These Functions into the Main Script

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

