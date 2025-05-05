from supportUDFs import CustomerSupportState

def determine_route(support_state: CustomerSupportState) -> str:
    """
    Route the inquiry based on sentiment and category.
    """
    if support_state["query_sentiment"] == "Negative":
        return "escalate_to_human_agent"
    elif support_state["query_category"] == "Vision":
        return "generate_vision_response"
    elif support_state["query_category"] == "Optimization":
        return "generate_optimised_path"
    else:
        return "generate_general_response"