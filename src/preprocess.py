import pandas as pd
import os
from datetime import datetime
RAW_PATH = "data/raw/news_posts.csv"
PROCESSED_PATH = "data/processed/news_clean.csv"

df = pd.read_csv(RAW_PATH)
print(f"Raw data loaded: {len(df)} articles")
print(df.isnull().sum()) # filtering out the bad data , data that has missing items in it 
df = df.dropna(subset=["title", "description"])
print(f"After removing missing values: {len(df)} articles")
df = df.drop_duplicates(subset=["title"])
print(f"After removing duplicates: {len(df)} articles")
df["published_at"] = pd.to_datetime(df["published_at"])
df["date"] = df["published_at"].dt.date
df["hour"] = df["published_at"].dt.hour
df["day_of_week"] = df["published_at"].dt.day_name()
print(df[["published_at", "date", "hour", "day_of_week"]].head())


df["title_length"] = df["title"].str.len()
df["description_length"] = df["description"].str.len()
print(df[["title", "title_length", "description_length"]].head())

now = datetime.now(df["published_at"].dt.tz)
df["hours_since_published"] = (now - df["published_at"]).dt.total_seconds() / 3600
df["trend_velocity"] = df["title_length"] / (df["hours_since_published"] + 1)
print(df[["title", "hours_since_published", "trend_velocity"]].head())


df.to_csv(PROCESSED_PATH, index=False)
print(f"\nClean data saved: {len(df)} articles")
print(f"Columns: {list(df.columns)}")