# dashboard_display.py

import streamlit as st
import pandas as pd

import pytz

def display_overall_section(final_sentiment, last_updated, sentiment_counts, text_data, sentiment_history, country="Hong Kong"):
    """Displays the main title, subtitle, and overall sentiment for a specific country with all parts in the right column."""

    # Define the color based on the final sentiment
    color = {
        "Positive": "#28a745",
        "Neutral": "#ffc107",
        "Negative": "#dc3545",
        "Mixed": "#6c757d"
    }.get(final_sentiment, "#6c757d")  # Default to gray if sentiment is not found

    st.markdown(
        """
        <style>
        .title-section { display: flex; justify-content: space-between; width: 100%; }
        .left-column { width: 25%; padding-right: 2rem; }
        .right-column { width: 75%; }
        .sentiment-box { 
            background-color: """ + color + """; padding: 2rem; border-radius: 10px; 
            text-align: center; color: white; font-weight: bold; width: 100%;
        }
        .sentiment-box p { font-size: 2.5rem; margin: 0; }
        .sentiment-box small { font-size: 1rem; color: #ccc; }
        .main-title { font-size: 2.5rem; font-weight: bold; color: #ddd; margin-bottom: 1rem; }
        .subtitle { color: #aaa; font-size: 1.1rem; margin-bottom: 1rem; }
        .country-label { color: #aaa; font-size: 1.5rem; font-weight: bold; margin-top: 1rem; }
        </style>
        """,
        unsafe_allow_html=True
    )

    col1, col2 = st.columns([1, 3])  # Adjust the column proportions as needed

    with col1:
        st.markdown(
            f"""
            <div class="main-title">Stock Market Sentiment Index</div>
            <div class="subtitle">Real-time insights on the sentiment driving the {country} stock market</div>
            """,
            unsafe_allow_html=True
        )

    with col2:
        # Main sentiment box
        st.subheader(f"Hong Kong")
        st.markdown(
            f"""
            <div class="sentiment-box">
                <p>{final_sentiment}</p>
                <small>Last updated: {last_updated.strftime("%Y-%m-%d %H:%M:%S %Z%z")} HKT</small>
            </div>
            """,
            unsafe_allow_html=True
        )

        # Sentiment breakdown
        display_sentiment_breakdown(sentiment_counts=sentiment_counts, country=country)

        # Detailed Analysis and Historical Data
        display_detailed_analysis(text_data, country=country)
        # display_historical_data(sentiment_history, country=country)



def display_sentiment_breakdown(sentiment_counts, country="Hong Kong"):
    """Displays sentiment breakdown for a specific country in the right column."""
    col1, col2, col3, col4 = st.columns(4)

    sentiment_icons = {
        "Positive": "😊",
        "Neutral": "😐",
        "Negative": "😟",
        "Mixed": "🔄"
    }

    for col, (sentiment, count) in zip([col1, col2, col3, col4], sentiment_counts.items()):
        icon = sentiment_icons[sentiment]
        with col:
            st.markdown(
                f"""
                <div style="text-align: center; font-size: 1.5rem;">{icon}</div>
                <div style="text-align: center; font-size: 1.2rem; font-weight: bold;">{count}</div>
                <div style="text-align: center; color: #777; font-size: 0.85rem;">{sentiment}</div>
                """,
                unsafe_allow_html=True
            )


def display_detailed_analysis(text_data, country="Hong Kong"):
    """Displays detailed sentiment analysis for a specific country in the right column."""
    with st.expander(f"Detailed Analysis"):
        for text_info in text_data:
            st.markdown(
                f"""
                <div style="border: 1px solid #ddd; border-radius: 8px; padding: 10px; margin-bottom: 10px;">
                    <strong>Source:</strong> {text_info['tag']}
                    <p style="font-style: italic;">"{text_info['text']}"</p>
                    <strong>Final Sentiment:</strong> {text_info['sentiment']}
                </div>
                """,
                unsafe_allow_html=True
            )

            for agent, agent_sentiment in text_info["details"].items():
                agent_name = agent.replace("_", " ").title()
                summarized_sentiment = agent_sentiment[:100] + "..."  # Summarize long text
                st.markdown(
                    f"<p><strong>{agent_name}:</strong> {summarized_sentiment}</p>",
                    unsafe_allow_html=True
                )


def display_historical_data(sentiment_history, country="Hong Kong"):
    """Displays historical sentiment data for a specific country in the right column."""
    if sentiment_history:
        history_df = pd.DataFrame(sentiment_history, columns=["Timestamp", "Sentiment"])
        sentiment_summary = history_df["Sentiment"].value_counts()
        st.bar_chart(sentiment_summary)
        st.write("Detailed History")
        st.dataframe(history_df)
