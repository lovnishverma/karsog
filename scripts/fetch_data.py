# scripts/fetch_data.py
import os
import json
import requests
from pymongo import MongoClient
from datetime import datetime

# 1. SETUP - Get Secrets from Environment
NEWS_API_KEY = os.environ.get('NEWS_API_KEY')
MONGO_URI = os.environ.get('MONGO_URI')

data_output = {
    "last_updated": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
    "news": [],
    "directory": [] 
}

# 2. FETCH NEWS
try:
    print("--- FETCHING NEWS ---")
    # CHANGED: Broadened query to "Himachal Pradesh" to ensure we get results
    url = f"https://newsapi.org/v2/everything?q=Himachal Pradesh&sortBy=publishedAt&language=en&apiKey={NEWS_API_KEY}"
    
    response = requests.get(url)
    if response.status_code == 200:
        articles = response.json().get("articles", [])
        # Filter out removed articles
        valid_articles = [a for a in articles if a['title'] != '[Removed]']
        data_output["news"] = valid_articles[:6] # Keep top 6
        print(f"Success: Found {len(valid_articles)} news articles.")
    else:
        print(f"News API Error: Status {response.status_code}")
        print(response.text)
except Exception as e:
    print(f"News Script Error: {e}")

# 3. FETCH MONGODB
try:
    print("\n--- FETCHING MONGODB ---")
    client = MongoClient(MONGO_URI)
    
    # DEBUG: Print all database names to help you find the right one
    print(f"Available Databases in Cluster: {client.list_database_names()}")

    # IMPORTANT: Make sure this matches one of the names printed above!
    db = client["karsog_db"] 
    collection = db["businesses"] 

    # Get all documents, exclude '_id'
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
    print("File saved to assets/site_data.json")
except Exception as e:
    print(f"Save Error: {e}")
