"""Vehicles Routing Problem (VRP)."""

from __future__ import print_function
from ortools.constraint_solver import routing_enums_pb2
from ortools.constraint_solver import pywrapcp
from math import radians, cos, sin, asin, sqrt


def haversine(lat1, lon1, lat2, lon2):
    """
    Calculate the great circle distance between two points
    on the earth (specified in decimal degrees)
    """
    # convert decimal degrees to radians
    lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lon2, lat2])

    # haversine formula
    dlon = lon2 - lon1
    dlat = lat2 - lat1
    a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
    c = 2 * asin(sqrt(a))
    r = 6371  # Radius of earth in kilometers. Use 3956 for miles
    return c * r


def distance_matrix_haversine(origin, destinations):
    """Convert origin and list of destination into distance matrix"""
    or_lat, or_lng = origin['lat'], origin['lng']
    locations = []
    locations.append((or_lat, or_lng))
    for destination in destinations:
        locations.append((destination['lat'], destination['lng']))
    matrix = []
    for m in locations:
        matrix_item = []
        for n in locations:
            if m == n:
                matrix_item.append(0)
            else:
                distance = haversine(m[0], m[1], n[0], n[1])
                matrix_item.append(distance)
        matrix.append(matrix_item)

    return matrix


def create_data_model(locations, num_vehicles):
    """Stores the data for the problem.

    :param locations: location that contains origin and destinations
        eg: {
            'origin': {'lat': -6.2173207, 'lng': 106.8315268},
            'destinations': [
                {'lat': -6.1826708, 'lng': 106.8679899},
                {'lat': -6.3627638, 'lng': 106.8270482},
            ]
        }
    """
    data = {}
    data['distance_matrix'] = distance_matrix_haversine(**locations)
    data['num_vehicles'] = num_vehicles
    data['depot'] = 0
    return data


class Routes:
    def __init__(self, locations, num_vehicles):
        self._locations = locations
        self._num_vehicles = num_vehicles

    def __assemble_response(self, data, manager, routing, solution):
        """Return the result in REST API friendly format"""
        max_route_distance = 0
        final = []
        for vehicle_id in range(data['num_vehicles']):
            res = {}
            res['sequence'] = []
            index = routing.Start(vehicle_id)
            res['vehicle_id'] = vehicle_id
            route_distance = 0
            while not routing.IsEnd(index):
                res['sequence'].append(manager.IndexToNode(index))
                previous_index = index
                index = solution.Value(routing.NextVar(index))
                route_distance += routing.GetArcCostForVehicle(
                    previous_index, index, vehicle_id)
            res['sequence'].append(manager.IndexToNode(index))
            res['total_distance'] = route_distance
            max_route_distance = max(route_distance, max_route_distance)
            final.append(res)
        return final

    def calculate(self):
        """Solve the CVRP problem."""
        # Instantiate the data problem.
        data = create_data_model(self._locations, self._num_vehicles)

        # Create the routing index manager.
        manager = pywrapcp.RoutingIndexManager(
            len(data['distance_matrix']), data['num_vehicles'], data['depot'])

        # Create Routing Model.
        routing = pywrapcp.RoutingModel(manager)

        # Create and register a transit callback.

        def distance_callback(from_index, to_index):
            """Returns the distance between the two nodes."""
            # Convert from routing variable Index to distance matrix NodeIndex.
            from_node = manager.IndexToNode(from_index)
            to_node = manager.IndexToNode(to_index)
            return data['distance_matrix'][from_node][to_node]

        transit_callback_index = routing.RegisterTransitCallback(distance_callback)

        # Define cost of each arc.
        routing.SetArcCostEvaluatorOfAllVehicles(transit_callback_index)

        # Add Distance constraint.
        dimension_name = 'Distance'
        routing.AddDimension(
            transit_callback_index,
            0,  # no slack
            3000,  # vehicle maximum travel distance
            True,  # start cumul to zero
            dimension_name)
        distance_dimension = routing.GetDimensionOrDie(dimension_name)
        distance_dimension.SetGlobalSpanCostCoefficient(100)

        # Setting first solution heuristic.
        search_parameters = pywrapcp.DefaultRoutingSearchParameters()
        search_parameters.first_solution_strategy = (
            routing_enums_pb2.FirstSolutionStrategy.PATH_CHEAPEST_ARC)

        # Solve the problem.
        solution = routing.SolveWithParameters(search_parameters)

        # Print solution on console.
        if solution:
            return self.__assemble_response(data, manager, routing, solution)
