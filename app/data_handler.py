import praw
import os
from dotenv import load_dotenv
import json
import pandas as pd
import requests


# Load environment variables from .env file
load_dotenv()

reddit = praw.Reddit(
    client_id=os.getenv("REDDIT_CLIENT_ID"),
    client_secret=os.getenv("REDDIT_CLIENT_SECRET"),
    password=os.getenv("REDDIT_PASSWORD"),  # Replace with your Reddit account password
    user_agent=os.getenv("REDDIT_USER_AGENT"),
    username=os.getenv("REDDIT_USERNAME")
)

# Verify Reddit instance is connected
print(f"Connected as: {reddit.user.me()}")

def fetch_reddit_data(subreddit_name="financialindependence", limit=5):
    subreddit = reddit.subreddit(subreddit_name)
    posts = []
    for submission in subreddit.hot(limit=limit):
        posts.append({
            "title": submission.title,
            "score": submission.score,
            "url": submission.url,
            "created_utc": submission.created_utc,
            "num_comments": submission.num_comments
        })
    return posts

def fetch_gdelt_data(query, max_records=10):
    url = f"https://api.gdeltproject.org/api/v2/doc/doc?query={query}&mode=artlist&maxrecords={max_records}&format=json"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        return data.get('articles', [])
    else:
        print("Error fetching GDELT data:", response.status_code)
        return []

def save_to_json(data, filename="data/reddit_data.json"):
    os.makedirs("data", exist_ok=True)  # Ensure 'data' directory exists
    with open(filename, "w") as f:
        json.dump(data, f, indent=4)

def convert_to_dataframe(data):
    return pd.DataFrame(data)
