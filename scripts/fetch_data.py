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

    # Query: We use the API to filter out obvious financial spam (-IPO, -Sensex)
    query = '"Karsog" OR "Mandi" OR "Himachal Pradesh" OR "Shimla" -IPO -Sensex'

    url = f"https://newsapi.org/v2/everything?q={query}&sortBy=publishedAt&language=en&apiKey={NEWS_API_KEY}"

    response = requests.get(url)
    if response.status_code == 200:
        all_articles = response.json().get("articles", [])

        # POSITIVE KEYWORDS (Article must have at least one)
        relevant_keywords = ["karsog", "sukhvinder singh sukhu", "pahadi", "suket",
                             "himachal", "shimla", "sundernagar", "manali", "kullu", "devbhoomi"]

        # NEGATIVE KEYWORDS (Article must have ZERO)
        # Added: 'furniss', 'walls', 'pagerduty', 'chatbot' to block the people named Mandi
        forbidden_keywords = [
            "3sbio", "ipo", "hong kong", "alibaba", "hair-loss", "weight-loss",
            "dividend", "sensex", "nifty", "trading", "bse", "nse",
            "furniss", "mandi walls", "pagerduty", "chatbot", "autistic", "ai chatbot"
        ]

        filtered_news = []
        for article in all_articles:
            # Cleaning
            if article['title'] == '[Removed]':
                continue

            # Normalize text for checking
            title = (article['title'] or "").lower()
            desc = (article['description'] or "").lower()
            full_text = title + " " + desc

            # CHECK 1: Must NOT contain forbidden words
            if any(bad_word in full_text for bad_word in forbidden_keywords):
                print(f"Skipped Irrelevant: {article['title'][:30]}...")
                continue

            # CHECK 2: Must contain at least one relevant keyword
            if any(word in full_text for word in relevant_keywords):
                filtered_news.append(article)

        # SORTING: Force 'Karsog' news to the top
        filtered_news.sort(key=lambda x: "karsog" not in (
            x['title'] or "").lower())

        data_output["news"] = filtered_news[:6]  # Keep top 6
        print(f"Success: Found {len(filtered_news)} clean articles.")
    else:
        print(f"News API Error: {response.text}")

except Exception as e:
    print(f"News Script Error: {e}")

# 3. FETCH MONGODB
try:
    print("\n--- FETCHING MONGODB ---")
    client = MongoClient(MONGO_URI)

    # UPDATE THIS LINE to match your Atlas Database Name
    # Based on your previous logs, if you didn't change it, try 'test' or 'karsog_db'
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
