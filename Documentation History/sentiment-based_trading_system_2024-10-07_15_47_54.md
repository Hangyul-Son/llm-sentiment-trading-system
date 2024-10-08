# Sentiment-Based Trading System_2024-10-07_15_47_54 Research Document

Created on: 2024-10-07 15:47:54

## 1. Literature Review

### Key Papers


- Explore papers on how sentiment impacts stock markets and macroeconomic indicators during recessions.
- Referenced Paper: "Designing Heterogeneous LLM Agents for Financial Sentiment Analysis" from ACM Digital Library.
  - This paper informed the approach to designing LLM agents tailored for financial sentiment analysis, particularly in heterogeneous market environments.


### Other Sentiment-Based Trading Systems


- Examine sentiment-based models applied in Asian markets and recession indicators.
- Study existing systems that combine news, social media, and financial forum sentiment, with insights drawn from LLM agents described in the referenced paper.


## 2. System Requirements

### Core Functionalities


1. Data collection from news articles, social media, company earnings calls, financial reports, and industry surveys.
2. Sentiment analysis focused on Southeast Asian equities and foreign institutional sentiment.
3. Country-specific sentiment tracking for the top five stocks of each market.
4. Incorporate insights from heterogeneous LLM agents to diversify sentiment analysis perspectives.


### Data Sources


#### News Data
- Bloomberg, Reuters, Financial Times, NewsAPI, GDELT.

#### Social Media Feeds
- Twitter API (tweepy) and Reddit (PRAW) for financial discussions.

#### Market Data
- Yahoo Finance API or IEX Cloud for HK-listed ADRs and alternative economic indicators (e.g., Consumer Confidence Index, PMI).


### Sentiment Analysis Approach


- Utilize GPT API to capture foreign perspectives on local markets and native sentiment on specific sectors.
- Based on the LLM agent design principles in the referenced paper, consider developing a multi-agent system for diversified sentiment perspectives.


## 3. Tools and Libraries Evaluation

### Sentiment Analysis


- GDELT for global event data and financial sentiment tracking across countries.
- Insights from LLM agents (referenced paper) may guide library selection for nuanced sentiment analysis.


### Financial Data APIs


1. Twitter API (tweepy)
2. Reddit API (PRAW)
3. Yahoo Finance (yfinance)
4. Alpha Vantage


### Other Relevant Libraries


- Integrate alternative economic indicators with pandas, NumPy for data handling, and matplotlib/plotly for visualization.


## 4. Project Outline

### High-Level System Architecture


- Components for categorizing news, social media, and financial forum sentiment.
- Foreign sentiment analysis on Southeast Asian stocks.
- Real-time dashboard for investor insights.
- Multi-agent architecture inspired by LLM agent designs from referenced paper for enriched sentiment analysis.


### Project Milestones


1. Develop a country-specific sentiment tracker.
2. Integrate multiple data sources and alternative indicators.
3. Complete a basic web dashboard for real-time insights.


## 5. Notes and Ideas

- Consider a sentiment momentum indicator based on macroeconomic indicators.
- Include sentiment analysis of foreign institutional reports on local equities.
- Build user-defined categories like economic events or central bank policies.
- Explore how multi-agent sentiment approaches from the referenced LLM paper could enhance real-time insights.


