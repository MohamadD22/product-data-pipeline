from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

def calculate_similarity(keyword, title, description):
    # Combine keyword, title, and description into a single string
    combined_texts = [keyword, title, description]
    
    # Create a TF-IDF Vectorizer
    vectorizer = TfidfVectorizer().fit_transform(combined_texts)
    vectors = vectorizer.toarray()
    
    # Calculate cosine similarity
    cosine_sim = cosine_similarity(vectors)
    
    # Similarity score between keyword and the product (title + description)
    return cosine_sim[0, 1]  # Cosine similarity between the first (keyword) and second (title + description) vectors

# Example usage within product fetching function
def fetch_aliexpress_products(keyword):
    url = f"https://www.aliexpress.com/wholesale?SearchText={keyword.strip()}"
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    products = []
    for item in soup.select('.JIIxO'):
        title = item.select_one('.JIIxO ._1OUGS ._2c4iS').text if item.select_one('.JIIxO ._1OUGS ._2c4iS') else 'No name'
        description = item.select_one('.JIIxO ._3R8Xy ._2YmoW ._3CnGk').text if item.select_one('.JIIxO ._3R8Xy ._2YmoW ._3CnGk') else 'No description'
        similarity_score = calculate_similarity(keyword, title, description)
        product = {
            'title': title,
            'link': item.select_one('a').get('href'),
            'price': description,  # Assuming price is part of description
            'similarity_score': similarity_score,
            'website': 'AliExpress'
        }
        products.append(product)
    return products
