import praw
import os
from dotenv import load_dotenv
import json
import pandas as pd
import requests

# Load environment variables from .env file
load_dotenv()

# Shared ranked keywords for both Reddit and GDELT
RANKED_KEYWORDS = [
    ["HSI", "Hang Seng", "Hong Kong Stocks", "Hong Kong Index", "Hang Seng Index"],  # Rank 1
    ["China", "Asia", "Singapore"],      # Rank 2
    ["US", "Global", "Something"]        # Rank 3
]
# List of subreddits to search
SUBREDDITS = ["HongKong", "stocks", "investing", "finance"]
num_data_per_source = 2

reddit = praw.Reddit(
    client_id=os.getenv("REDDIT_CLIENT_ID"),
    client_secret=os.getenv("REDDIT_CLIENT_SECRET"),
    password=os.getenv("REDDIT_PASSWORD"),  # Replace with your Reddit account password
    user_agent=os.getenv("REDDIT_USER_AGENT"),
    username=os.getenv("REDDIT_USERNAME")
)

# Verify Reddit instance is connected
print(f"Connected as: {reddit.user.me()}")

def fetch_reddit_data(limit=5):
    """Fetches posts from specified subreddits based on ranked keywords."""
    for rank, keywords in enumerate(RANKED_KEYWORDS, start=1):
        print(f"Searching Rank {rank} keywords: {keywords}")
        posts = []

        for subreddit_name in SUBREDDITS:
            subreddit = reddit.subreddit(subreddit_name)
            for keyword in keywords:
                for submission in subreddit.search(keyword, limit=limit):
                    posts.append({
                        "title": submission.title,
                        "score": submission.score,
                        "url": submission.url,
                        "created_utc": submission.created_utc,
                        "num_comments": submission.num_comments,
                        "subreddit": subreddit_name
                    })
                
                # Stop searching lower ranks if we find posts
                if len(posts) >= num_data_per_source:
                    return pd.DataFrame(posts)
        
    # If no posts found in any rank
    print("No Reddit posts found for any of the ranked keywords.")
    return pd.DataFrame()

def fetch_gdelt_data_with_ranking(max_records=10):
    """Fetches articles from GDELT based on ranked keywords."""
    for rank, keywords in enumerate(RANKED_KEYWORDS, start=1):
        keyword_query = "(" + " OR ".join(keywords) + ")"
        query = f'{keyword_query} AND (domain:reuters.com OR domain:yahoo.com OR domain:cnbc.com) AND sourcelang:english'
        print(f"Trying Rank {rank} keywords: {query}")
        articles = fetch_gdelt_data(query, max_records)
        
        if len(articles) >= num_data_per_source:
            # Print the first article's keys for inspection
            print("Sample article keys:", articles[0].keys())
            return pd.DataFrame(articles)

    print("No articles found.")
    return pd.DataFrame()


def fetch_gdelt_data(query, max_records=10):
    """Helper function to retrieve GDELT data for a specific query."""
    url = "https://api.gdeltproject.org/api/v2/doc/doc"
    params = {
        "query": query,
        "mode": "ArtList",
        "format": "json",
        "maxrecords": max_records,
        "sort": "DateDesc"
    }
    response = requests.get(url, params=params)
    if response.status_code == 200:
        data = response.json()
        return data.get('articles', [])
    else:
        print("Error fetching GDELT data:", response.status_code)
        return []
    
def convert_to_dataframe(data):
    return pd.DataFrame(data)
