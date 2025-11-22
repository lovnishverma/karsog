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

# 2. FETCH NEWS (STRICT FILTERING)
try:
    print("--- FETCHING NEWS ---")
    # Broad query to get candidates
    query = '"Karsog" OR "Mandi" OR "Himachal Pradesh" OR "Shimla"'
    url = f"https://newsapi.org/v2/everything?q={query}&sortBy=publishedAt&language=en&apiKey={NEWS_API_KEY}"
    
    response = requests.get(url)
    if response.status_code == 200:
        all_articles = response.json().get("articles", [])
        
        # KEYWORDS WE CARE ABOUT
        relevant_keywords = ["karsog", "mandi", "himachal", "shimla", "sundernagar"]
        
        filtered_news = []
        for article in all_articles:
            # content checks
            title = (article['title'] or "").lower()
            desc = (article['description'] or "").lower()
            
            # Remove [Removed] articles
            if "removed" in title:
                continue

            # STRICT CHECK: Keyword must be in Title or Description
            if any(word in title for word in relevant_keywords) or \
               any(word in desc for word in relevant_keywords):
                filtered_news.append(article)

        # Sort: Karsog news first!
        filtered_news.sort(key=lambda x: "karsog" not in (x['title'] or "").lower())

        data_output["news"] = filtered_news[:6] # Keep top 6 strictly relevant
        print(f"Success: Found {len(filtered_news)} relevant articles.")
    else:
        print(f"News API Error: {response.text}")

except Exception as e:
    print(f"News Script Error: {e}")

# 3. FETCH MONGODB
try:
    print("\n--- FETCHING MONGODB ---")
    client = MongoClient(MONGO_URI)
    
    # DEBUG: Help find the correct DB name
    print(f"Available DBs: {client.list_database_names()}")
    
    # UPDATE THIS LINE if your DB name is different in the log!
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
