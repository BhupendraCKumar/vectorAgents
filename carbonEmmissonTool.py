from supportUDFs import CustomerSupportState
# from langchain_core.tools import tool
from llmCall import toolCall

# import ormsgpack


import ormsgpack
import pandas as pd

def serialize_dataframe(df):
    return df.to_dict()

def deserialize_dataframe(data):
    return pd.DataFrame.from_dict(data)


def convert_keys_to_str(data):
    if isinstance(data, dict):
        return {str(key): convert_keys_to_str(value) for key, value in data.items()}
    elif isinstance(data, list):
        return [convert_keys_to_str(element) for element in data]
    else:
        return data

# # Convert DataFrame to dictionary
# data_dict = df.to_dict()

# # Serialize using ormsgpack
# packed_data = ormsgpack.packb(data_dict)

def compute_emission_savings(state: CustomerSupportState) -> CustomerSupportState:
    # Assume emission rate
    emission_rate = 0.25  # kg CO₂ per km for delivery van

    # Distance covered in naive order
    naive_route = list(range(len(state['addresses'])))
    distance_matrix = state['distance_matrix']
    # print("LENGTHS : ", len(naive_route),len(distance_matrix))
    # Sum up naive route distance
    naive_distance = sum(
        distance_matrix[naive_route[i]][naive_route[i+1]]
        for i in range(len(naive_route) - 1)
    )

    # Sum up optimized route distance
    # print("LENGTH OF TSP ROUTE : ", len(tsp_route))
    tsp_route = state['tsp_route']
    optimized_distance = sum(
        distance_matrix[tsp_route[i]][tsp_route[i+1]]
        for i in range(len(tsp_route) - 1)
    )

    # Compute emissions
    original_emissions = naive_distance * emission_rate
    optimized_emissions = optimized_distance * emission_rate
    emissions_saved = original_emissions - optimized_emissions

    final_response = f'''\nCarbon Emissions Report:
    Naive Route Distance: {naive_distance:.2f} km → CO₂: {original_emissions:.2f} kg \n
    Optimized Route Distance: {optimized_distance:.2f} km → CO₂: {optimized_emissions:.2f} kg \n
    Carbon Emissions Saved: {emissions_saved:.2f} kg CO₂'''

    packed_parcels = state['packing_summary']
    df = state['organized_parcels']
    addresses = df['address'].to_list()
    # tsp_route = state.get('tsp_route')
    # packed_parcels = msgpack.packb(packed_parcels)
    # print("FINAL STATE : ", state) 
    #
    final_response_prompt = f""" 
    You are an agent for an AI products and hardware manufacturing company. Which is trying to help to optimize the solution to reduce carbon footprint.

    Please read the outputs analysed by an intelligent agent below based on which generate a human understandable response,
    Based on the query understand which parameter are important to generate a reponse.

    The following is the packing result of parcels into a delivery container:
    {packed_parcels}
    Please:
    - List the items packed in order.
    - Describe where each item is placed (position).
    - Explain how this order helps with delivery (i.e., items delivered later are packed deeper).
    - Generate a friendly human-readable summary considering the below responses speciall final response.
    Order in parcels to be delivered: {addresses},
    final_response= {final_response},
    """
    # {packed_parcels}
    # print("FINAL PROMPT ",final_response_prompt)
    state['final_response'] = toolCall(final_response_prompt)
    # update the state
    state['addresses'] = ormsgpack.packb(state['addresses'])
    state['distance_matrix']= ormsgpack.packb(state['distance_matrix'])
    state['organized_parcels'] = ormsgpack.packb(convert_keys_to_str(serialize_dataframe(state['organized_parcels'])))
    state['tsp_route'] = ormsgpack.packb(state['tsp_route'])
    # state['packing_summary'] =None

    # print("FINAL STATE : ",state)
    return (state)
