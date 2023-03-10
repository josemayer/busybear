import json
import os
import requests
import math
import functions.utils

def authenticate():
    config = functions.utils.get_json_data("config/API.json")
    auth_config = config["auth"]
    auth_key = os.environ.get("AUTH_SPTRANS_KEY")
    auth_url = auth_config["api_URL"] + auth_key

    auth_response = requests.post(auth_url)
    return auth_response

def get_data(url):
    try:
        get_response = requests.get(url)
        get_response.raise_for_status()
    except requests.exceptions.HTTPError as e:
        if e.response.status_code == 401:
            auth_response = authenticate()
            headers = {
                "Cookie": auth_response.headers["Set-Cookie"]
            }
            get_response = requests.get(url, headers=headers)
        else:
            raise e
    
    data = get_response.json()
    return data

def retrieve_buses(way):
    config = functions.utils.get_json_data("config/API.json")
    buses_config = config["buses"]

    if way != 'p3' and way != 'butanta':
        return []

    lines = buses_config["ways_lc"][way]
    buses = []
    for line in lines:
        data_URL = buses_config["api_URL"] + str(lines[line])
        data = get_data(data_URL)
        
        vehicles = data["vs"]

        for vehicle in vehicles:
            bus = {
                "bus_line": line,
                "bus_code": vehicle["p"],
                "lat": vehicle["py"],
                "lng": vehicle["px"]
            }

            buses.append(bus)

    return buses

def buses_at_points_with_way(way):
    buses = retrieve_buses(way)
    points = functions.utils.get_json_data("data/points.json")
    routes = functions.utils.get_json_data("data/routes.json")
    buses_and_points = []
    for bus in buses:
        bus_location = (bus["lat"], bus["lng"])
        points_on_route = [point for point in points if point["id"] in routes[bus["bus_line"]][way]]
        closest_point = functions.geolocator.closest_point(bus_location, points_on_route)
        
        buses_and_points.append({
            "bus": bus,
            "point": closest_point
        })

    return buses_and_points

def rank_points(candidate_points, localization, buses_and_points, way):
    routes = functions.utils.get_json_data("data/routes.json")
    
    points_distance = {}
    for point in candidate_points:
       for bus in buses_and_points:
            bus_line = bus["bus"]["bus_line"]
            if point["id"] in routes[bus_line][way]:
                point_position = routes[bus_line][way].index(point["id"])
                bus_position = routes[bus_line][way].index(bus["point"]["id"])
                # Check if the point id in the route has greater index than the point id of the bus
                if point_position > bus_position:
                    if not point["id"] in points_distance:
                        points_distance[point["id"]] = {
                            "titulo": point["titulo"],
                            "lat": point["lat"],
                            "lng": point["lng"],
                            "buses": []
                        }

                    # Calculate the points distance (difference of indexes) of the bus and the point
                    difference = point_position - bus_position
                    # Add the difference to the list of buses of the point
                    bus_info = {
                        "bus_line": bus_line,
                        "bus_code": bus["bus"]["bus_code"],
                        "bus_point": bus["point"],
                        "distance": difference
                    }
                    points_distance[point["id"]]["buses"].append(bus_info)

    return points_distance
