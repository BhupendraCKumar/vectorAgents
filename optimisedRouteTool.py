import openrouteservice
from ortools.constraint_solver import routing_enums_pb2, pywrapcp
# from langchain_core.tools import tool
from supportUDFs import CustomerSupportState
# import certifi
# import requests
# session = requests.Session()
# session.verify = certifi.where()

ORS_API_KEY = ""


# @tool
def compute_distances(state:CustomerSupportState):
    client = openrouteservice.Client(key=ORS_API_KEY,requests_kwargs={'verify':False})
    addresses = state['addresses']
    locations = [client.pelias_search(text=addr)['features'][0]['geometry']['coordinates'] for addr in addresses]

    matrix = client.distance_matrix(locations, metrics=["distance"], units="km")['distances']
    state['distance_matrix'] = matrix
    return state

# @tool
def solve_tsp(state:CustomerSupportState):
    print("COMPUTING DISTANCES ")
    state = compute_distances(state)
    distanceMatrix = state['distance_matrix']

    print("COMPUTED DISTANCE MATRICES : ", distanceMatrix)
    manager = pywrapcp.RoutingIndexManager(len(distanceMatrix), 1, 0)
    routing = pywrapcp.RoutingModel(manager)

    def distanceCallback(from_index, to_index):
        return int(distanceMatrix[manager.IndexToNode(from_index)][manager.IndexToNode(to_index)])

    transitCallbackIndex = routing.RegisterTransitCallback(distanceCallback)

    routing.SetArcCostEvaluatorOfAllVehicles(transitCallbackIndex)

    search_parameters = pywrapcp.DefaultRoutingSearchParameters()
    search_parameters.first_solution_strategy = (routing_enums_pb2.FirstSolutionStrategy.PATH_CHEAPEST_ARC)

    solution = routing.SolveWithParameters(search_parameters)

    if solution:
        index = routing.Start(0)
        route = []
        while not routing.IsEnd(index):
            route.append(manager.IndexToNode(index))
            index = solution.Value(routing.NextVar(index))
        route.append(manager.IndexToNode(index))
        state['tsp_route'] = route

        return state
    else:
        return None
