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
        response = requests.get(
            url, params=params, headers=headers, timeout=10)
        response.raise_for_status()  # Raise an HTTPError for bad responses (4xx and 5xx)

        # Check if the response contains valid JSON
        if response.headers.get("Content-Type") == "application/json" or response.headers.get("Content-Type") == "application/json; charset=utf-8":
            data = response.json()
            if data:
                return float(data[0]['lat']), float(data[0]['lon']), None
            else:
                return None, None, error
        else:
            print(
                f"Unexpected response type: {response.headers.get('Content-Type')}")
            print(f"Response text: {response.text}")
            error = "Unexpected response type"
    except requests.exceptions.RequestException as e:
        print(f"Error fetching data from the API: {e}")
        error = "Error fetching data from the API"
    except (ValueError, KeyError) as e:
        print(f"Error parsing response JSON: {e}")
        error = "Error parsing response JSON"

    return None, None, error


def optimal_route(location_coordinates):
    route = []
    base_coordinates = []
    error = None
    for i in range(len(location_coordinates)):
        location_coordinates[i] = location_array[i].strip()
        latitude, longitude, error = get_coordinates(location_coordinates[i])
        base_coordinates.append({"name": location_coordinates[i], "coordiantes": [
                                float(latitude), float(longitude)], "error": error})

    # use symetric TSP to find the optimal route
    # using nearest neighbor algorithm

    # initialize the route with the start point
    start_point = base_coordinates[0]["coordiantes"]
    start_location_name = base_coordinates[0]["name"]
    print("Start point coordinates: ", start_point,
          "Start Location name: ", start_location_name)
    route = [{"coordinates": start_point, "location": start_location_name}]
    base_coordinates.pop(0)
    # for _ in range(2):  # for testing
    #     print("Coordinates: ", base_coordinates)
    #     # find the nearest neighbor
    #     route_for = route[-1]["coordinates"]
    #     nearest_neighbour(base_coordinates, route_for, route)

    return route, error


def get_route(coordinates):
    # coordinates = [[lat1, lon1], [lat2, lon2]]
    coord_str = ";".join([f"{coord[1]},{coord[0]}" for coord in coordinates])
    osrm_url = f"http://router.project-osrm.org/route/v1/driving/{coord_str}?overview=full&geometries=geojson"

    response = requests.get(osrm_url)
    if response.status_code == 200:
        return response.json()
    else:
        return {"error": "Unable to fetch route from OSRM"}


def nearest_neighbour(location_coordinates):
    route = []
    error = None
    # remove the start location from location_coordinates and add to route
    route.append(location_coordinates[0])
    location_coordinates.pop(0)
    # now find the nearest neighbour to the last coordinate in location_coordinates
    nearest_neighbour = None
    nearest_distance = None
    for coords in location_coordinates:

    return route, error
