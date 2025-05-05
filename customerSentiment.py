from supportUDFs import CustomerSupportState,QuerySentiment
from llmCall import toolCall

def analyze_inquiry_sentiment( support_state: CustomerSupportState) -> CustomerSupportState:
    """
    Analyze the sentiment of the customer query as Positive, Neutral, or Negative.
    """

    query = support_state["customer_query"]
    SENTIMENT_CATEGORY_PROMPT = """Act as a customer support agent trying to best categorize the customer query's sentiment.
                                   You are an agent for an AI products and hardware manufacturing company. Which is trying to help to optimize the solution to reduce carbon footprint.

                                   Please read the customer query below,
                                   analyze its sentiment which should be one from the following list:

                                   'Positive', 'Neutral', or 'Negative'.

                                   Return just the sentiment (from one of the above)

                                   Query:
                                   {customer_query}
                                """
    prompt = SENTIMENT_CATEGORY_PROMPT.format(customer_query=query)
    sentiment_category = toolCall(prompt,True,QuerySentiment)

    return {
        "query_sentiment": sentiment_category.sentiments}