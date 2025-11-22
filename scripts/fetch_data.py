# scripts/fetch_data.py
import os
import json
import requests
from pymongo import MongoClient
from datetime import datetime

# 1. SETUP
NEWS_API_KEY = os.environ.get('NEWS_API_KEY')
MONGO_URI = os.environ.get('MONGO_URI')

data_output = {
    "last_updated": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
    "news": [],
    "directory": [] 
}

# 2. FETCH NEWS (SMART FILTERING)
try:
    print("--- FETCHING NEWS ---")
    
    # UPDATED QUERY: Added negative keywords (-) to block irrelevant topics at the source
    # We block 'IPO', '3SBio' (the pharma company), and 'Sensex' (irrelevant stock news)
    query = '"Karsog" OR "Mandi" OR "Himachal Pradesh" OR "Shimla" -IPO -3SBio -Sensex'
    
    url = f"https://newsapi.org/v2/everything?q={query}&sortBy=publishedAt&language=en&apiKey={NEWS_API_KEY}"
    
    response = requests.get(url)
    if response.status_code == 200:
        all_articles = response.json().get("articles", [])
        
        # POSITIVE KEYWORDS (Must have at least one)
        relevant_keywords = ["karsog", "mandi", "himachal", "shimla", "sundernagar", "manali", "kullu"]
        
        # NEGATIVE KEYWORDS (Must have ZERO)
        # If an article contains these, we trash it immediately
        forbidden_keywords = ["3sbio", "ipo", "hong kong", "alibaba", "hair-loss", "weight-loss", "dividend", "sensex", "nifty"]

        filtered_news = []
        for article in all_articles:
            # Cleaning
            if article['title'] == '[Removed]': continue
            
            # Normalize text for checking
            title = (article['title'] or "").lower()
            desc = (article['description'] or "").lower()
            full_text = title + " " + desc

            # CHECK 1: Must NOT contain forbidden words
            if any(bad_word in full_text for bad_word in forbidden_keywords):
                print(f"Skipped Irrelevant Article: {article['title'][:30]}...")
                continue

            # CHECK 2: Must contain at least one relevant keyword
            if any(word in full_text for word in relevant_keywords):
                filtered_news.append(article)

        # SORTING: Force 'Karsog' news to the top
        # This lambda function puts articles with "karsog" at index 0 (False < True in sorting)
        filtered_news.sort(key=lambda x: "karsog" not in (x['title'] or "").lower())

        data_output["news"] = filtered_news[:6] # Keep top 6
        print(f"Success: Found {len(filtered_news)} clean articles.")
    else:
        print(f"News API Error: {response.text}")

except Exception as e:
    print(f"News Script Error: {e}")

# 3. FETCH MONGODB
try:
    print("\n--- FETCHING MONGODB ---")
    client = MongoClient(MONGO_URI)
    
    # DEBUG: This prints your DB names so you can verify them in the GitHub logs
    print(f"Available DBs: {client.list_database_names()}")
    
    # UPDATE THIS LINE if your DB name is different in the log!
    # Common defaults: 'test', 'admin', 'karsog_db'
    db = client["karsog_db"] 
    collection = db["businesses"] 

    documents = list(collection.find({}, {"_id": 0}))
    data_output["directory"] = documents
    print(f"Success: Found {len(documents)} directory items.")
    
except Exception as e:
    print(f"Mongo Script Error: {e}")

# 4. SAVE
try:
    os.makedirs("assets", exist_ok=True)
    with open("assets/site_data.json", "w") as f:
        json.dump(data_output, f, indent=2)
    print("\n--- SAVED SUCCESSFULLY ---")
except Exception as e:
    print(f"Save Error: {e}")
