import praw
import os
from dotenv import load_dotenv
import json
import pandas as pd
import requests
import streamlit as st
from datetime import datetime, timedelta
import pytz

# Load environment variables from .env file
load_dotenv()

# Shared ranked keywords for both Reddit and GDELT
RANKED_KEYWORDS = [
    # Rank 1: Hong Kong-Specific Market Terms (with Reddit-Appropriate Keywords)
    [
        "HSI", "Hang Seng", "HK Stocks", "Hong Kong Stock Exchange", "HKEX", 
        "Hang Seng Index", "Hong Kong Investments", "Hong Kong Equities", 
        "HK Trading", "Hang Seng Futures", "Hang Seng Tech", "HK Market", 
        "Hong Kong Stocks Discussion", "Hong Kong Stocks News", "HK Finance", 
        "HSI Analysis"
    ],
    
    # Rank 2: Broader Asian Market Keywords
    [
        "China Stock Market", "Shanghai Composite", "Shenzhen Index", 
        "Singapore Stock Exchange", "Asian Markets", "China Economy", 
        "Singapore Stocks", "Nikkei Index", "KOSPI", "Asian Stocks", 
        "ASEAN Markets", "China Stocks", "Asian Financial News"
    ],

    # Rank 3: Global Financial and Economic Keywords
    [
        "US Stock Market", "Dow Jones", "S&P 500", "NASDAQ", "US Federal Reserve", 
        "Global Markets", "World Stocks", "Investment Trends", "US Economy", 
        "Global Trading", "Interest Rates", "Global Economic Outlook", 
        "US Inflation", "Crypto Market"
    ]
]

# List of subreddits to search
SUBREDDITS = ["HongKong", "stocks", "investing", "finance"]
num_data_per_source = 2

reddit = praw.Reddit(
    client_id=st.secrets["REDDIT_CLIENT_ID"],
    client_secret=st.secrets["REDDIT_CLIENT_SECRET"],
    # password=st.secrets["REDDIT_PASSWORD"],  # Replace with your Reddit account password
    user_agent=st.secrets["REDDIT_USER_AGENT"],
    # username=st.secrets["REDDIT_USERNAME"]
)

# Verify Reddit instance is connected
print(f"Connected as: {reddit.user.me()}")

def fetch_reddit_data(limit=5):
    """Fetches recent posts from specified subreddits based on ranked keywords in the past hour."""
    one_hour_ago = datetime.now(pytz.utc) - timedelta(hours=1)  # Get the time one hour ago in UTC

    for rank, keywords in enumerate(RANKED_KEYWORDS, start=1):
        print(f"Searching Rank {rank} keywords: {keywords}")
        posts = []

        for subreddit_name in SUBREDDITS:
            subreddit = reddit.subreddit(subreddit_name)
            
            # Fetch the latest posts from the subreddit
            for submission in subreddit.new(limit=limit * len(keywords)):
                submission_time = datetime.utcfromtimestamp(submission.created_utc).replace(tzinfo=pytz.utc)
                print(submission.title.lower())
                # Check if the post is within the last hour and contains any of the ranked keywords
                if submission_time >= one_hour_ago:
                    if any(keyword.lower() in submission.title.lower() for keyword in keywords):
                        posts.append({
                            "title": submission.title,
                            "score": submission.score,
                            "url": submission.url,
                            "created_utc": submission.created_utc,
                            "num_comments": submission.num_comments,
                            "subreddit": subreddit_name
                        })
                    
                
                # Stop searching lower ranks if we find enough posts
                if len(posts) >= num_data_per_source:
                    return pd.DataFrame(posts)

    # If no posts found in any rank
    print("No Reddit posts found for any of the ranked keywords in the past hour.")
    return pd.DataFrame()


def fetch_gdelt_data_with_ranking(max_records=10):
    """Fetches articles from GDELT based on ranked keywords in the past hour."""
    one_hour_ago = datetime.now(pytz.utc) - timedelta(hours=1)
    one_hour_ago_str = one_hour_ago.strftime("%Y%m%d%H%M%S")  # Format suitable for GDELT (e.g., 20241010153000)

    for rank, keywords in enumerate(RANKED_KEYWORDS, start=1):
        keyword_query = "(" + " OR ".join(keywords) + ")"
        # Adding date range filter to GDELT query
        query = f'{keyword_query} AND (domain:reuters.com OR domain:yahoo.com OR domain:cnbc.com) AND sourcelang:english'
        print(f"Trying Rank {rank} keywords: {query}")
        articles = fetch_gdelt_data(query, max_records)
        
        if len(articles) >= num_data_per_source:
            # Print the first article's keys for inspection
            print("Sample article keys:", articles[0].keys())
            return pd.DataFrame(articles)

    print("No articles found in the past hour.")
    return pd.DataFrame()

def fetch_gdelt_data(query, max_records=10):
    """Helper function to retrieve GDELT data for a specific query."""
    url = "https://api.gdeltproject.org/api/v2/doc/doc"
    params = {
        "query": query,
        "mode": "ArtList",
        "format": "json",
        "maxrecords": max_records,
        "sort": "DateDesc",
        "timespan": "1h"
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
