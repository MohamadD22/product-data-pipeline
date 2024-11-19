# product-data-pipeline
The aim of this project is to This project automates the retrieval of product data from AliExpress and multimedia content from YouTube based on keywords entered in a Google Sheets document. The retrieved data is then populated into specified sheets within the document.

## Setup Instructions

### Prerequisites
- Python 3.x
- Virtual environment tool (venv)
- Google Cloud Project with API credentials
- YouTube Data API v3 key

### Steps
1. **Clone the Repository**:
   ```bash
   git clone https://github.com/MohamadD22/product-data-pipeline.git
   cd product-data-pipeline
   
Create a Virtual Environment:

**bash**
python -m venv venv
venv\Scripts\activate   # On Windows
source venv/bin/activate # On MacOS/Linux
Install Dependencies:

**bash:**
pip install -r requirements.txt
Configure API Keys:

Place your credentials.json file in the project directory.

Obtain a YouTube Data API key and replace your_youtube_api_key in the script with your actual key.

Share Google Sheet with Service Account:

Open your Google Sheet.

Share the sheet with the service account email found in your credentials.json file and grant "Editor" permissions.

**Usage**
**Enter Keywords:**

Open the Google Sheet and enter keywords in the "User Input" sheet starting from cell A2.

Run the Script:

**bash**
venv\Scripts\activate  # On Windows
source venv/bin/activate # On MacOS/Linux
python fetch_products.py


**Challenges Faced**

Fetching AliExpress Data: Encountered difficulties with scraping due to website structure changes.

Google Sheets Integration: Ensured proper sharing and permissions for service accounts.

**Development Decisions**
Algorithm Choice: Used TF-IDF and cosine similarity for keyword-product matching.

**Error Handling:**
Implemented robust exception handling to manage API request failures and network issues.

**Future Enhancements**
Support for Additional E-commerce Websites: Extend the script to fetch product data from other e-commerce websites.

**Enhanced Data Analysis:**
Implement more sophisticated data analysis and reporting features.

**Error Handling:**
Improve error handling to manage edge cases and unexpected responses.

