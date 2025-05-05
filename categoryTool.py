
from supportUDFs import CustomerSupportState, QueryCategory
from llmCall import toolCall

def categorize_inquiry(support_state: CustomerSupportState) -> CustomerSupportState:
    """
    Classify the customer query into Vision, Optimization, or General.
    """

    query = support_state["customer_query"]
    print("QUERY CATEGORY FILE : ",query)
    ROUTE_CATEGORY_PROMPT = """Act as a customer support agent trying to best categorize the customer query.
                               You are an agent for an AI products and hardware company.

                               Please read the customer query below and
                               determine the best category from the following list:

                               'Vision', 'Optimization', or 'General'.

                               Remember:
                                - Vision queries will focus more on vision related queries, to perform quality check in product images, shape of the objects in an image etc.
                                - General queries will focus more on general aspects like contacting support, finding things, policies etc.
                                - Optimization queries will focus more on optimizing the route given a file with addresses or arranging parcels in a truck/container to optimize the space.

                                Return just the category name (from one of the above)

                                Query:
                                {customer_query}
                            """
    prompt = ROUTE_CATEGORY_PROMPT.format(customer_query=query)
    
    route_category = toolCall(prompt,True,QueryCategory)
    print("CATEGORY ", route_category)
    return {
        "query_category": route_category.categorized_topic
    }