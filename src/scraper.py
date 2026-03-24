import requests
import pandas as pd
from dotenv import load_dotenv
import os
from datetime import datetime

load_dotenv()

API_KEY = os.getenv("NEWS_API_KEY")

categories = ["technology", "science", "business", "health", "sports"]

posts = []

for category in categories:
    print(f"Fetching {category} news...")
    
    url = "https://newsapi.org/v2/top-headlines"
    params = {
        "category": category,
        "language": "en",
        "pageSize": 100,
        "apiKey": API_KEY
    }
    
    response = requests.get(url, params=params)
    data = response.json()
    
    if data["status"] == "ok":
        for article in data["articles"]:
            posts.append({
                "title": article["title"],
                "source": article["source"]["name"],
                "category": category,
                "published_at": article["publishedAt"],
                "url": article["url"],
                "description": article["description"]
            })
        print(f"  Got {len(data['articles'])} articles")
    else:
        print(f"  Error: {data}")

df = pd.DataFrame(posts)
df.to_csv("data/raw/news_posts.csv", index=False)
print(f"\nDone! Scraped {len(df)} articles. Saved to data/raw/news_posts.csv")