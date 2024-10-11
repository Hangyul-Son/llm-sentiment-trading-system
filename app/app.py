import streamlit as st
import streamlit.components.v1 as components
from data_handler import fetch_reddit_data, fetch_gdelt_data_with_ranking, convert_to_dataframe
from sentiment_service import analyze_sentiment

st.title("Hong Kong Stock Market Sentiment Index")
st.write("Welcome to the Sentiment Index Dashboard")

# Fetch GDELT data with keyword ranking
try:
    gdelt_data = fetch_gdelt_data_with_ranking(max_records=5)
    print(gdelt_data)
    if not gdelt_data.empty:
        # Adjust column names based on available fields
        st.write("**GDELT Data**")
        st.dataframe(gdelt_data[["title", "url"]])  # Use actual available columns


        # Display each article's title with an expandable section for additional metadata
        for _, row in gdelt_data.iterrows():
            with st.expander(row["title"]):
                st.write(f"**Date**: {row.get('publishedDate', 'Date not available')}")
                st.write(f"[Read Full Article]({row['url']})")  # Link to full article
    else:
        st.write("No GDELT articles found for the given keywords.")
except Exception as e:
    st.error(f"An error occurred while fetching GDELT data: {e}")


# Fetch Reddit data based on ranked keywords
try:
    reddit_data = fetch_reddit_data(limit=5)
    if not reddit_data.empty:
        st.write("**Reddit Data**")
        st.dataframe(reddit_data[["title", "subreddit", "score", "num_comments", "url"]])  # Display key details in table

        # Display each post's title with an expandable section for additional metadata
        for _, row in reddit_data.iterrows():
            with st.expander(row["title"]):
                st.write(f"**Subreddit**: {row['subreddit']}")
                st.write(f"**Score**: {row['score']}")
                st.write(f"**Comments**: {row['num_comments']}")
                st.write(f"[Read Full Post]({row['url']})")  # Link to the post
    else:
        st.write("No Reddit posts found for the given keywords.")
except Exception as e:
    st.error(f"An error occurred while fetching Reddit data: {e}")



# # Fetch one post
# try:
#     reddit_data = fetch_reddit_data(subreddit_name="financialindependence", limit=1)
#     title = reddit_data[0]["title"]
#     print(title)

#     # Perform sentiment analysis
#     analysis_result = analyze_sentiment(title)
#     aggregated_sentiment, agent_sentiments = analysis_result["final_sentiment"], analysis_result["agent_sentiments"]

#     print(aggregated_sentiment)
#     # Display the result
#     st.write("**Post Title:**", title)

#     # Display aggregated sentiment in a big and shiny way
#     if aggregated_sentiment.lower() == "positive":
#         sentiment_color = "#28a745"  # green
#     elif aggregated_sentiment.lower() == "negative":
#         sentiment_color = "#dc3545"  # red
#     elif aggregated_sentiment.lower() == "neutral":
#         sentiment_color = "#ffc107"  # yellow
#     elif aggregated_sentiment.lower() == "mixed":
#         sentiment_color = "#6c757d"  # gray
#     else:
#         sentiment_color = "#000000"  # black for unexpected values

#     st.markdown(f"""
#         <div style="text-align: center; font-size: 48px; font-weight: bold; color: {sentiment_color};">
#             {aggregated_sentiment}
#         </div>
#     """, unsafe_allow_html=True)

#     st.write("**Sentiment of each agent:**")
#     for agent, sentiment in agent_sentiments.items():
#         st.write(f"- **{agent}:** {sentiment}")

# except IndexError:
#     st.error("No posts were fetched. Please check the subreddit or try again later.")
# except Exception as e:
#     st.error(f"An error occurred: {e}")
