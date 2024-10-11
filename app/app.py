import streamlit as st
from datetime import datetime, timedelta
import pandas as pd
from sentiment_service import analyze_sentiment
from dashboard_display import (
    display_overall_section, display_sentiment_breakdown,
    display_detailed_analysis, display_historical_data
)
from data_handler import fetch_reddit_data, fetch_gdelt_data_with_ranking


UPDATE_INTERVAL = timedelta(hours=1)
last_updated = datetime.now() - UPDATE_INTERVAL  # Force initial load
sentiment_history = []

def get_sentiment_analysis():
    """Fetches data from Reddit and GDELT, performs sentiment analysis, and returns aggregated results."""
    gdelt_data = fetch_gdelt_data_with_ranking(max_records=2)
    reddit_data = fetch_reddit_data(limit=2)

    text_data = []
    if not gdelt_data.empty:
        for _, row in gdelt_data.iterrows():
            result = analyze_sentiment(row["title"])
            refined_sentiment = result["final_sentiment"].capitalize()
            text_data.append({
                "text": row["title"],
                "tag": "Financial News",
                "sentiment": refined_sentiment,
                "details": result["agent_sentiments"]
            })

    if not reddit_data.empty:
        for _, row in reddit_data.iterrows():
            result = analyze_sentiment(row["title"])
            refined_sentiment = result["final_sentiment"].capitalize()
            text_data.append({
                "text": row["title"],
                "tag": "Financial Forum Data",
                "sentiment": refined_sentiment,
                "details": result["agent_sentiments"]
            })

    # Aggregate sentiment counts
    sentiment_counts = pd.Series([item['sentiment'] for item in text_data]).value_counts()
    sentiment_counts = sentiment_counts.reindex(["Positive", "Neutral", "Negative", "Mixed"], fill_value=0)
    final_sentiment = sentiment_counts.idxmax()
    sentiment_history.append((datetime.now(), final_sentiment))

    return final_sentiment, sentiment_counts.to_dict(), text_data

# In your main display function, use the following
def display_dashboard():
    global last_updated
    if datetime.now() - last_updated >= UPDATE_INTERVAL:
        final_sentiment, sentiment_counts, text_data = get_sentiment_analysis()
        last_updated = datetime.now()

        # Display various dashboard sections with the updated layout
# Example of calling display_overall_section in your main app file (app.py)
        display_overall_section(final_sentiment, last_updated, sentiment_counts, text_data, sentiment_history, country="Hong Kong")


if __name__ == "__main__":
    st.set_page_config(layout="wide")
    display_dashboard()
