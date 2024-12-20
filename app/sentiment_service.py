import os
import openai

# Instantiate the client using environment variable for the API key
client = openai.OpenAI(
    api_key=os.environ.get("OPENAI_API_KEY"),
)

# Main function to analyze sentiment using different agents
def analyze_sentiment(content):
    print(f"Starting sentiment analysis for '''{content}'''\n\n")
    agent_functions = [
        mood_agent,
        institutional_investor_agent,
        # individual_investor_agent,
        # rhetoric_agent,
        # dependency_agent,
        # aspect_agent,
        # reference_agent
    ]
    responses = {agent.__name__: agent(content) for agent in agent_functions}
    print("All initial agent responses collected.")
    
    final_sentiment, final_agent_responses = summative_agent(responses)
    
    return {"agent_sentiments": final_agent_responses, "final_sentiment": final_sentiment}

# Function to determine final sentiment by aggregating agent responses
def summative_agent(responses, max_rounds=2):
    round_count = 0
    consensus_reached = False
    high_priority_agents = ["institutional_investor_agent", "individual_investor_agent"]
    sentiment_summary = responses.copy()

    while not consensus_reached and round_count < max_rounds:
        combined_responses = combine_agent_responses(sentiment_summary)
        
        overall_sentiment = get_overall_sentiment(combined_responses)
        
        if overall_sentiment in ["positive", "negative", "neutral"]:
            consensus_reached = True
            final_sentiment = overall_sentiment.capitalize()
        else:
            round_count += 1
            sentiment_summary = refine_agent_responses(sentiment_summary, combined_responses)

    if not consensus_reached:
        final_sentiment = get_high_priority_sentiment(sentiment_summary, high_priority_agents)

    print(f"Final sentiment determined: {refine_final_sentiment(final_sentiment)}\n\n")
    return final_sentiment, sentiment_summary

# Helper function to combine responses from all agents
def combine_agent_responses(sentiment_summary):
    return "\n".join([f"{agent}: {response}" for agent, response in sentiment_summary.items()])

# Helper function to get overall sentiment from GPT-4
def get_overall_sentiment(combined_responses):
    try:
        response = client.chat.completions.create(
            model="gpt-4-turbo",
            messages=[
                {"role": "user", "content": f"Based on the following responses from various agents, summarize the overall sentiment as Positive, Negative, Neutral, or Mixed:  \n\n{combined_responses} \n The overall sentiment 'MUST' be a single word from Positive, Negative, Neutral, or Mixed. Your response should be a single word and that is final."}
            ]
        )
        return response.choices[0].message.content.strip().lower()
    except Exception as e:
        print(f"Error in overall sentiment summary request: {str(e)}")
        return "error"

# Helper function to refine agent responses
def refine_agent_responses(sentiment_summary, combined_responses):
    refined_summary = {}
    for agent, response in sentiment_summary.items():
        try:
            refined_response = client.chat.completions.create(
                model="gpt-4-turbo",
                messages=[
                    {"role": "user", "content": f"Refine your sentiment analysis by reviewing these responses:\n{combined_responses}\nOriginal response: {response} \n Please keep your analysis 'Concise'"}
                ]
            )
            refined_summary[agent] = refined_response.choices[0].message.content
        except Exception as e:
            print(f"Error refining response for {agent}: {str(e)}")
            refined_summary[agent] = "Error in refining response"
    return refined_summary

# Helper function to get final sentiment from high-priority agents
def get_high_priority_sentiment(sentiment_summary, high_priority_agents):
    high_priority_responses = "\n".join(
        [f"{agent}: {sentiment_summary[agent]}" for agent in high_priority_agents if agent in sentiment_summary]
    )
    try:
        final_response = client.chat.completions.create(
            model="gpt-4-turbo",
            messages=[
                {"role": "user", "content": f"Summarize the final sentiment based on high-priority agents alone:\n{high_priority_responses}\n The overall sentiment 'MUST' be a single word from Positive, Negative, Neutral, or Mixed. Your response should be a single word and that is final."}
            ]
        )
        return final_response.choices[0].message.content.strip().capitalize()
    except Exception as e:
        print(f"Error summarizing final sentiment with high-priority agents: {str(e)}")
        return "Error in final consensus"

import re

def refine_final_sentiment(sentiment):
    # Normalize to lowercase and strip extra whitespace
    sentiment = sentiment.strip().lower()

    # Common sentiment categories and variants, including misspellings and phrasing variations
    positive_variants = [
        "positive", "very positive", "mostly positive", "slightly positive", 
        "somewhat positive", "quite positive", "positive trend", "upward trend", 
        "bullish", "optimistic", "growing confidence", "positve", "posiitve", "positiv"
    ]
    
    negative_variants = [
        "negative", "very negative", "mostly negative", "slightly negative",
        "somewhat negative", "quite negative", "negative trend", "downward trend", 
        "bearish", "pessimistic", "declining confidence", "negitive", "negitive trend", 
        "negetive", "downward treand", "pessimisstic", "pessimistic trend"
    ]
    
    neutral_variants = [
        "neutral", "balanced", "no opinion", "neutral outlook", "stable", "unchanged", 
        "flat", "no strong opinion", "indifferent", "neutral stance", "nutral", 
        "neutrel", "balnced", "no opnion", "no opinnion"
    ]
    
    mixed_variants = [
        "mixed", "ambiguous", "uncertain", "inconclusive", "mixed signals", 
        "fluctuating", "volatile", "conflicted", "both positive and negative", 
        "unclear trend", "miixed", "mixxed", "ambigous", "fluctuating", "volitile", "unclear"
    ]

    # Helper function for substring matching with a list of variants
    def match_sentiment(variants):
        for variant in variants:
            # Using regex for approximate matching
            if re.search(rf"\b{variant}\b", sentiment):
                return True
        return False

    # Match sentiment to closest category
    if match_sentiment(positive_variants):
        return "positive"
    elif match_sentiment(negative_variants):
        return "negative"
    elif match_sentiment(neutral_variants):
        return "neutral"
    elif match_sentiment(mixed_variants):
        return "mixed"
    else:
        # Default to "mixed" if sentiment is not recognized
        return "mixed"

# Define each agent function
def mood_agent(content):
    return run_agent("Analyze the mood of this message, focusing on any hypothetical or speculative language that could affect sentiment:", content)

def institutional_investor_agent(content):
    return run_agent("Analyze this message as if you are an institutional investor, focusing on long-term impacts on stability and growth potential:", content)

def individual_investor_agent(content):
    return run_agent("Analyze this message as if you are an individual investor, focusing on short-term price impact and immediate gains or losses:", content)

def rhetoric_agent(content):
    return run_agent("Analyze the rhetorical style of this message, such as sarcasm, exaggeration, or assertive statements, and how these elements affect sentiment:", content)

def dependency_agent(content):
    return run_agent("Focus on the speaker’s sentiment in this message, without considering external perspectives or opinions of third parties:", content)

def aspect_agent(content):
    return run_agent("Analyze the sentiment toward the main entity (e.g., company or stock ticker) in this message, ignoring unrelated information:", content)

def reference_agent(content):
    return run_agent("Identify references to time, price points, or external factors in this message, and analyze how they impact the overall sentiment:", content)

# Helper function to run individual agents
def run_agent(prompt, content):
    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": f"{prompt} {content}"}]
        )
        return response.choices[0].message.content
    except Exception as e:
        print(f"Error processing agent: {str(e)}")
        return "Error in processing"
