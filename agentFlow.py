from langgraph.graph import StateGraph, END
from langgraph.checkpoint.memory import MemorySaver
from categoryTool import categorize_inquiry
from customerSentiment import analyze_inquiry_sentiment
from visionTool import analyze_images
from generalResponseTool import generate_general_response
from supportUDFs import CustomerSupportState
from esclationAgent import escalate_to_human_agent
from routeNode import determine_route
from carbonEmmissonTool import compute_emission_savings
from packParcelsTool import container_packing
from optimisedRouteTool import solve_tsp

# Create the graph with our typed state
carbon_emission_graph = StateGraph(CustomerSupportState)

# Add nodes for each function
carbon_emission_graph.add_node("categorize_inquiry", categorize_inquiry)
carbon_emission_graph.add_node("analyze_inquiry_sentiment", analyze_inquiry_sentiment)
carbon_emission_graph.add_node("generate_vision_response", analyze_images)
carbon_emission_graph.add_node("generate_general_response", generate_general_response)
carbon_emission_graph.add_node("escalate_to_human_agent", escalate_to_human_agent)
carbon_emission_graph.add_node("generate_optimised_path", solve_tsp)
carbon_emission_graph.add_node("generate_optimised_packing", container_packing)
carbon_emission_graph.add_node("carbon_emission_calculator_agent", compute_emission_savings)

# Add edges to represent the processing flow
carbon_emission_graph.add_edge("categorize_inquiry", "analyze_inquiry_sentiment")
carbon_emission_graph.add_conditional_edges(
    "analyze_inquiry_sentiment",
    determine_route,
    [
        "generate_vision_response",
        "generate_general_response",
        "escalate_to_human_agent",
        "generate_optimised_path",
    ]
)

# All terminal nodes lead to the END
carbon_emission_graph.add_edge("generate_optimised_path", "generate_optimised_packing")

carbon_emission_graph.add_edge("generate_optimised_packing", "carbon_emission_calculator_agent")
carbon_emission_graph.add_edge("carbon_emission_calculator_agent", END)

carbon_emission_graph.add_edge("generate_vision_response", END)
carbon_emission_graph.add_edge("generate_general_response", END)
carbon_emission_graph.add_edge("escalate_to_human_agent", END)

# Set carbon_emission_graph the entry point for the workflow
carbon_emission_graph.set_entry_point("categorize_inquiry")

# Compile the graph into a runnable agent
memory = MemorySaver()
compiled_carbon_emmission_agent = carbon_emission_graph.compile(checkpointer=memory)