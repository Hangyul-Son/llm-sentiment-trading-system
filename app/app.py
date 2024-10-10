import streamlit as st
import streamlit.components.v1 as components
from data_handler import fetch_reddit_data, fetch_gdelt_data, convert_to_dataframe
from sentiment_service import analyze_sentiment

st.title("Hong Kong Stock Market Sentiment Index")
st.write("Welcome to the Sentiment Index Dashboard")

# Fetch one post
try:
    reddit_data = fetch_reddit_data(subreddit_name="financialindependence", limit=1)
    title = reddit_data[0]["title"]
    print(title)

    # Perform sentiment analysis
    analysis_result = analyze_sentiment(title)
    aggregated_sentiment, agent_sentiments = analysis_result["final_sentiment"], analysis_result["agent_sentiments"]

    print(aggregated_sentiment)
    # Display the result
    st.write("**Post Title:**", title)

    # Display aggregated sentiment in a big and shiny way
    if aggregated_sentiment.lower() == "positive":
        sentiment_color = "#28a745"  # green
    elif aggregated_sentiment.lower() == "negative":
        sentiment_color = "#dc3545"  # red
    elif aggregated_sentiment.lower() == "neutral":
        sentiment_color = "#ffc107"  # yellow
    elif aggregated_sentiment.lower() == "mixed":
        sentiment_color = "#6c757d"  # gray
    else:
        sentiment_color = "#000000"  # black for unexpected values

    st.markdown(f"""
        <div style="text-align: center; font-size: 48px; font-weight: bold; color: {sentiment_color};">
            {aggregated_sentiment}
        </div>
    """, unsafe_allow_html=True)

    st.write("**Sentiment of each agent:**")
    for agent, sentiment in agent_sentiments.items():
        st.write(f"- **{agent}:** {sentiment}")

except IndexError:
    st.error("No posts were fetched. Please check the subreddit or try again later.")
except Exception as e:
    st.error(f"An error occurred: {e}")

# # Fetch GDELT data
# gdelt_data = fetch_gdelt_data(query="Hong Kong stock market", max_records=5)
# gdelt_df = convert_to_dataframe(gdelt_data)
# st.write("GDELT Data")
# st.dataframe(gdelt_df)