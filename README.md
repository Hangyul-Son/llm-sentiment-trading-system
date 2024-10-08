# LLM-Based Sentiment Index

This project builds an LLM-based Sentiment Index by analyzing financial and news data to produce a comprehensive market sentiment indicator. The system leverages large language models (LLMs) and a multi-agent framework to generate sentiment scores based on insights from financial data.

## System Overview

The LLM-based sentiment index system is designed with the following components:

1. **Data Collection**: Collects financial and news data from various sources.
2. **Data Preprocessing**: Cleans and prepares data for analysis.
3. **LLM-Based Sentiment Analysis**: Uses advanced language models to analyze sentiment from the preprocessed data.
4. **Sentiment Index Calculation**: Aggregates individual sentiment scores into a comprehensive sentiment index.
5. **Visualization and Reporting**: Presents the sentiment index in interactive dashboards and reports.

The diagram below illustrates the system architecture:

![System Diagram](./System%20Diagram/SystemDiagram_v0.1_20241008-Phase1.png)

> **Note**: Ensure the image file is located at `./System Diagram/SystemDiagram_v0.1_20241008-Phase1.png`. For issues, verify file permissions or consider hosting the image online and updating the link accordingly.

---

## Tools and Libraries

The project uses the following tools and libraries:

- **Python 3.7+**: The core programming language.
- **OpenAI API**: For GPT-based sentiment analysis.
- **TextBlob**: For additional NLP-based sentiment scoring.
- **Jupyter Notebook**: For interactive testing and development.

To install the necessary packages, run:

```bash
pip install openai textblob
```

## Methodology

This project replicates the multi-agent sentiment analysis approach from the referenced research paper. The system consists of several agents, each analyzing sentiment from different perspectives. Here’s a summary of the methodology:

1. **Agent Setup**:
   - Each agent is configured with a unique prompt to analyze sentiment based on a particular perspective (e.g., Mood, Institutional Investor, Individual Investor).
   
2. **Multi-Round Consensus**:
   - If agents don’t reach a consensus on sentiment, a **multi-round discussion** is initiated. Agents review each other's responses in iterative rounds, refining their outputs to reach a consensus.

3. **Summative Agent**:
   - The Summative Agent aggregates responses and, if consensus remains inconclusive, defers to high-priority agents to guide the final sentiment decision. Sentiment outcomes can be **Positive**, **Negative**, **Neutral**, or **Mixed**.