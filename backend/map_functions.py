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
    headers = {'User-Agent': Config.OSM_HEADER}
    url = "https://api.openrouteservice.org/v2/directions/driving-car"
    coordinates = []
    error = None
    for i in range(len(location_array)):
        location_array[i] = location_array[i].strip()
        latitude, longitude, error = get_coordinates(location_array[i])
        coordinates.append({"name": location_array[i], "coordiantes": [ latitude, longitude], "error": error})
    
