import requests
from config import Config



def get_coordinates(location):
    url = "https://nominatim.openstreetmap.org/search"
    params = {
        "q": location.strip(),
        "format": "json",
        "addressdetails": 1,
        "limit": 1,
    }

    headers = {'User-Agent': Config.OSM_HEADER}
    error = None
    
    try:
        response = requests.get(url, params=params,headers=headers, timeout=10)
        response.raise_for_status()  # Raise an HTTPError for bad responses (4xx and 5xx)
        
        # Check if the response contains valid JSON
        if response.headers.get("Content-Type") == "application/json" or response.headers.get("Content-Type") == "application/json; charset=utf-8":
            data = response.json()
            if data:
                return data[0]['lat'], data[0]['lon'], error
            else:
                return None, None, error
        else:
            print(f"Unexpected response type: {response.headers.get('Content-Type')}")
            print(f"Response text: {response.text}")
            error = "Unexpected response type"
    except requests.exceptions.RequestException as e:
        print(f"Error fetching data from the API: {e}")
        error = "Error fetching data from the API"
    except (ValueError, KeyError) as e:
        print(f"Error parsing response JSON: {e}")
        error = "Error parsing response JSON"
    
    return None, None, error


def optimal_route(location_array):
    
    base_coordinates = []
    error = None
    for i in range(len(location_array)):
        location_array[i] = location_array[i].strip()
        latitude, longitude, error = get_coordinates(location_array[i])
        base_coordinates.append({"name": location_array[i], "coordiantes": [ float(latitude), float(longitude)], "error": error})
    
    # use symetric TSP to find the optimal route
    # using nearest neighbor algorithm

    # initialize the route with the start point
    start_point = base_coordinates[0]["coordiantes"]
    start_location_name = base_coordinates[0]["name"]
    print("Start point coordinates: ",start_point, "Start Location name: ", start_location_name)
    route = [{"coordinates": start_point, "location": start_location_name}]
    base_coordinates.pop(0)
    while base_coordinates:
        print("Coordinates: ", base_coordinates)
        # find the nearest neighbor
        route_for = route[-1]["coordinates"]
        nearest_neighbour(base_coordinates, route_for, route)
            
        
    return route, error
    


def nearest_neighbour(base_coordinates, route_for, route):
    # find the nearest neighbor to the route_for in the base_coordinates
    # return the nearest neighbor and
    # the distance between the route_for and the nearest neighbor
    # remove the nearest neighbor from the base_coordinates and add to route
    nearest_neighbor = None
    nearest_distance = None
    start_coords = route_for
    for location in base_coordinates:
        end_coords = location["coordiantes"]
        url = "https://api.openrouteservice.org/v2/directions/driving-car"
        headers = {
            "Authorization": Config.ORS_API_TOKEN,
            "Content-Type": "application/json"
        }
        payload = {
            "coordinates": [start_coords, end_coords],
            "units": "m"  # or "km" for kilometers
        }
        try:
            response = requests.get(url, json=payload, headers=headers, timeout=10)
            response.raise_for_status()  # Raise an HTTPError for bad responses (4xx and 5xx)
            
            # Check if the response contains valid JSON
            if response.headers.get("Content-Type") == "application/json" or response.headers.get("Content-Type") == "application/json; charset=utf-8":
                data = response.json()
                if data:
                    distance = data["routes"][0]["summary"]["distance"]
                    if not nearest_distance or distance < nearest_distance:
                        nearest_distance = distance
                        nearest_neighbor = location
                else:
                    print("No data in response")
            else:
                print(f"Unexpected response type: {response.headers.get('Content-Type')}")
                print(f"Response text: {response.text}")
        except requests.exceptions.RequestException as e:
            print(f"Error fetching data from the API: {e}")
        except (ValueError, KeyError) as e:
            print(f"Error parsing response JSON: {e}")
        if nearest_neighbor:
            route.append({"coordinates": nearest_neighbor["coordiantes"], "location": nearest_neighbor["name"]})
            base_coordinates.remove(nearest_neighbor)
