# scripts/fetch_data.py
import os
import json
import requests
from pymongo import MongoClient
from datetime import datetime

# 1. SETUP - Get Secrets
NEWS_API_KEY = os.environ.get('NEWS_API_KEY')
MONGO_URI = os.environ.get('MONGO_URI')

data_output = {
    "last_updated": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
    "news": [],
    "directory": [] 
}

# 2. FETCH NEWS (The "Smart Sort" Method)
try:
    print("--- FETCHING NEWS ---")
    # Query: Look for Karsog FIRST, then Mandi (District), then general HP news
    # The API will return a mix of all three.
    query = '"Karsog" OR "Mandi district" OR "Himachal Pradesh"'
    url = f"https://newsapi.org/v2/everything?q={query}&sortBy=publishedAt&language=en&apiKey={NEWS_API_KEY}"
    
    response = requests.get(url)
    if response.status_code == 200:
        all_articles = response.json().get("articles", [])
        
        # CLEANING: Remove [Removed] articles
        clean_articles = [a for a in all_articles if a['title'] != '[Removed]']

        # SORTING: Force 'Karsog' news to the top, then 'Mandi', then others
        karsog_news = []
        mandi_news = []
        general_news = []

        for article in clean_articles:
            title = article['title'].lower()
            desc = (article['description'] or "").lower()
            
            if "karsog" in title or "karsog" in desc:
                karsog_news.append(article)
            elif "mandi" in title or "mandi" in desc:
                mandi_news.append(article)
            else:
                general_news.append(article)

        # Combine them: Karsog First -> Mandi Second -> Rest
        final_list = karsog_news + mandi_news + general_news
        
        # Keep top 6
        data_output["news"] = final_list[:6]
        
        print(f"Success! Found: {len(karsog_news)} Karsog, {len(mandi_news)} Mandi, {len(general_news)} HP articles.")
    else:
        print(f"News API Error: {response.text}")

except Exception as e:
    print(f"News Script Error: {e}")

# 3. FETCH MONGODB
try:
    print("\n--- FETCHING MONGODB ---")
    client = MongoClient(MONGO_URI)
    
    # Ensure you use the exact Database Name from your Atlas Dashboard
    # If your DB is named 'test' or 'admin' in Atlas, change it here!
    db = client["karsog_db"] 
    collection = db["businesses"] 

    documents = list(collection.find({}, {"_id": 0}))
    data_output["directory"] = documents
    print(f"Success: Found {len(documents)} directory items.")
    
except Exception as e:
    print(f"Mongo Script Error: {e}")

# 4. SAVE TO FILE
try:
    os.makedirs("assets", exist_ok=True)
    with open("assets/site_data.json", "w") as f:
        json.dump(data_output, f, indent=2)
    print("\n--- SAVED SUCCESSFULLY ---")
except Exception as e:
    print(f"Save Error: {e}")
