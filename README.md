# LLM-Based Stock Market Sentiment Index

This project builds a real-time LLM-based Stock Market Sentiment Index by analyzing financial data from news sources and social media to provide a comprehensive market sentiment indicator. Using large language models (LLMs) within a multi-agent framework, this system generates sentiment scores based on insights from market-relevant data sources, including news and financial forums.

## System Overview

The LLM-based sentiment index system is designed with the following components:

1. **Data Collection**: Aggregates financial and news data from sources like GDELT and Reddit (e.g., Hong Kong-focused financial forums).
2. **Data Preprocessing**: Cleans and structures data to be suitable for LLM analysis.
3. **LLM-Based Sentiment Analysis**: Uses advanced language models to determine sentiment from the preprocessed data.
4. **Sentiment Index Calculation**: Aggregates individual sentiment scores into a comprehensive market sentiment index, with categories such as **Positive**, **Neutral**, **Negative**, and **Mixed**.
5. **Visualization and Reporting**: Presents the sentiment index in an interactive Streamlit dashboard for user-friendly insights.

The current implementation focuses on the **Hong Kong Stock Market**, with a flexible structure ready to support additional countries in the future.

---

## System Architecture

The diagram below outlines the system architecture:

![System Diagram](./System%20Diagram/System%20Diagram_v0.2_20241009.png)

> **Note**: Ensure the image file is located at `System Diagram/System Diagram_v0.2_20241009.png`. For issues, verify file permissions or consider hosting the image online and updating the link accordingly.

---

## Features

- **Country-Specific Sentiment Display**: The dashboard currently supports Hong Kong, with a layout that can easily be expanded to include other countries.
- **Dynamic Sentiment Breakdown**: Sentiment breakdown includes categories such as **Positive**, **Neutral**, **Negative**, and **Mixed**, displayed with intuitive icons and counters.
- **Expandable Detailed Analysis**: Users can view a breakdown of each data point analyzed, including sources and individual agent sentiment responses.
- [UNDER DEVELOPMENT] **Historical Sentiment Data**: View sentiment trends over time to identify shifts in market mood, with historical data visualized in interactive charts.

---

## Tools and Libraries

The project uses the following tools and libraries:

- **Python 3.7+**: The core programming language.
- **OpenAI API**: For GPT-based sentiment analysis.
- **Streamlit**: For building the interactive dashboard.
- **Jupyter Notebook**: For testing and development.
- **Pandas**: For data manipulation and processing.
---

## Methodology

This project replicates a multi-agent sentiment analysis approach inspired by the paper "Designing Heterogeneous LLM Agents for Financial Sentiment Analysis". The system includes several agents, each tasked with analyzing sentiment from a unique perspective. Here’s a summary of the methodology:

1. **Agent Setup**:
   - Each agent is designed with a distinct prompt, focusing on different perspectives (e.g., Mood Agent, Institutional Investor, Individual Investor).
   
2. **Multi-Round Consensus**:
   - If agents don’t initially reach a consensus on sentiment, a **multi-round discussion** is triggered. In each round, agents review each other's feedback, iteratively refining their outputs to converge on a consensus.

3. **Summative Agent**:
   - The Summative Agent consolidates agent responses, defaulting to high-priority agents when consensus remains inconclusive. Final sentiment outcomes are classified as **Positive**, **Neutral**, **Negative**, or **Mixed**.

---

## Dashboard Overview

The interactive Streamlit dashboard displays the sentiment index with an attractive, user-friendly interface. The main sections include:

1. **Real-Time Sentiment Summary**:
   - Displays the current sentiment for the Hong Kong Stock Market, and is updated **EVERY HOUR** automatically
   
2. **Sentiment Breakdown**:
   - An icon-based sentiment breakdown that provides a visual overview of **Positive**, **Neutral**, **Negative**, and **Mixed** sentiment counts.

3. **Detailed Sentiment Analysis**:
   - Expandable section displaying individual data points and agent-based sentiment assessments, allowing users to see how each piece of data was classified.

4. [UNDER DEVELOPMENT] **Historical Sentiment Data**:
   - Time-series visualization of sentiment trends over time, providing insights into historical market sentiment shifts.

---

## Future Enhancements

Planned improvements for future phases include:

- **Multi-Country Support**: Adding additional markets (e.g., US, UK, Japan) to provide a broader perspective on global market sentiment.
- **Enhanced Sentiment Granularity**: Extending agent analysis for deeper sentiment insights, potentially introducing more nuanced sentiment categories.
- **Expanded Data Sources**: Integrating more financial news and social media sources to improve data diversity and sentiment accuracy.

---

## Installation and Setup

To set up the project locally:

1. **Clone the repository**:
   ```bash
   git clone https://github.com/Hangyul-Son/llm-sentiment-trading-system.git
   cd LLM-based-sentiment-index
2. **Install Dependencies**: Ensure you have Python 3.7+ installed, then install dependencies:
   ```bash
   pip install -r requirements.txt
3. **Run the Streamlit Dashboard**: Ensure you have Python 3.7+ installed, then install dependencies:
   ```bash
   streamlit run app/app.py
   
Navigate to http://localhost:8501 to view the dashboard.
