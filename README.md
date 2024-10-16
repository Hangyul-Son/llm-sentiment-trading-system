﻿# LLM-Based Stock Market Sentiment Index

This project builds a real-time LLM-based Stock Market Sentiment Index by analyzing financial data from finanicla news sources, financial forums, social media and financial statements, etc, to provide a  sentiment for stock markets. Using large language models (LLMs) based on the recently published paper [Designing Heterogeneous LLM Agents for Financial Sentiment Analysis](https://arxiv.org/html/2401.05799v1), this system labels a final sentiment on the stock market as **Positive**, **Neutral**, **Negative**, and **Mixed**.

---

## Dashboard Service Overview

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

---

## System Overview

The LLM-based sentiment index system is designed with the following components:

1. **Data Collection & Processing**: Aggregates financial text data from sources like Financial Times, CNBC, and Reddit Financial Forums. Cleans and structures data to be suitable for LLM analysis.
2. **Sentiment Analysis Service**: Uses gpt based language models to determine sentiment from the preprocessed data.
3. **Dashboard**: Presents the sentiment of the stockmarket through a Streamlit dashboard. Update new sentiment every 1 hour.

The current implementation focuses on the **Hong Kong Stock Market**, with a flexible structure ready to support additional countries and assets in the future.

---

## System Architecture

The diagram below outlines the system architecture:

![System Diagram](./System%20Diagram/System%20Diagram_v0.2_20241009.png)

> **Note**: Ensure the image file is located at `System Diagram/System Diagram_v0.2_20241009.png`. For issues, verify file permissions or consider hosting the image online and updating the link accordingly.

---

## Tools and Libraries

The project uses the following tools and libraries:

- **Python 3.7+**: The core programming language.
- **OpenAI API**: For GPT-based sentiment analysis.
- **Reddit API**: For financial data collection
- **GDELTS API**: For financial data collection
- **Streamlit**: For building the interactive dashboard.
- **Jupyter Notebook**: For testing and development.
- **Pandas**: For data manipulation and processing.
---

## Sentiment Analysis Methodology

This project replicates a multi-agent sentiment analysis approach inspired by the paper "Designing Heterogeneous LLM Agents for Financial Sentiment Analysis". The system includes several agents, each tasked with analyzing sentiment from a unique perspective. Here’s a summary of the methodology:

Please refer to the file `app/sentiment_service.py` for details.

1. **Agent Setup**:
   - Each agent is designed with a distinct prompt, focusing on different perspectives (e.g., Mood Agent, Institutional Investor, Individual Investor).
   
2. **Multi-Round Consensus**:
   - If agents don’t initially reach a consensus on sentiment, a **multi-round discussion** is triggered. In each round, agents review each other's feedback, iteratively refining their outputs to converge on a consensus.

3. **Summative Agent**:
   - The Summative Agent consolidates agent responses, defaulting to high-priority agents when consensus remains inconclusive. Final sentiment outcomes are classified as **Positive**, **Neutral**, **Negative**, or **Mixed**.

---

## Future Enhancements

Planned improvements for future phases include:

- **Multi-Country Support**: Adding additional markets (e.g., US, UK, Japan) to provide a broader perspective on global market sentiment.
- **Enhanced Sentiment Granularity**: Extending agent analysis for deeper sentiment insights, potentially introducing more nuanced sentiment categories.
- **Expanded Data Sources**: Integrating more financial news and social media sources to improve data diversity and sentiment accuracy.
