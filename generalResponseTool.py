
from supportUDFs import CustomerSupportState
from langchain_core.prompts import ChatPromptTemplate
from llmCall import toolCall

def generate_general_response(support_state: CustomerSupportState) -> CustomerSupportState:
    """
    Provide a general support response by combining knowledge from the LLM.
    """
    # Retrieve category and ensure it is lowercase for metadata filtering
    categorized_topic = support_state["query_category"]
    query = support_state["customer_query"]

    # Use metadata filter for 'general' queries
    if categorized_topic.lower() == "general":
        
        # Combine retrieved information into the prompt
        prompt = f"""
            Craft a clear and detailed general support response for the following customer query.
            In case there is no knowledge base information or you do not know the answer just say:

            Apologies I was not able to answer your question, please reach out to +1-xxx-xxxx

            Customer Query:
            {query}
            """
        
        # Generate the final response using the LLM
        general_reply = toolCall(prompt)
    else:
        # For non-general queries, provide a default response or a general handling
        general_reply = "Apologies I was not able to answer your question, please reach out to +1-xxx-xxxx"

    # Update and return the modified support state
    return {
        "final_response": general_reply
    }
