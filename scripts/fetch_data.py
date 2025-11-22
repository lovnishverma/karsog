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
    "directory": []  # From MongoDB
}

# 2. FETCH NEWS (Only 1 call per run!)
try:
    print("Fetching News...")
    url = f"https://newsapi.org/v2/everything?q=Karsog&apiKey={NEWS_API_KEY}"
    response = requests.get(url)
    if response.status_code == 200:
        data_output["news"] = response.json().get(
            "articles", [])[:6]  # Keep top 6
except Exception as e:
    print(f"News Error: {e}")

# 3. FETCH MONGODB (Securely!)
try:
    print("Fetching MongoDB...")
    client = MongoClient(MONGO_URI)
    db = client["karsog_db"]  # Change to your DB name
    collection = db["businesses"]  # Change to your collection

    # Get all documents, exclude '_id' because it's not JSON serializable
    documents = list(collection.find({}, {"_id": 0}))
    data_output["directory"] = documents
except Exception as e:
    print(f"Mongo Error: {e}")

# 4. SAVE TO FILE
# We save this to the 'assets' folder so your website can read it
os.makedirs("assets", exist_ok=True)
with open("assets/site_data.json", "w") as f:
    json.dump(data_output, f, indent=2)

print("Data update complete!")
