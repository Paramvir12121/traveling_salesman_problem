from flask import Flask, render_template, request, jsonify
import requests

app = Flask(__name__)

headers = {'User-Agent': 'PathFinder/1.0 (paramvir.singh.ic@gmail.com)' }

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/route-finder')
def get_route_page():
    return render_template('route.html', route=None)


@app.route('/get-route', methods=['POST'])
def get_route():
    addresses = [request.form['address1'], request.form['address2'], request.form['address3']]
    coordinates = []

    for address in addresses:
        if address:
            coord = get_coordinates_from_address(address)
            if coord:
                coordinates.append(coord)

    if len(coordinates) < 2:
        return "<p>At least two valid addresses are required</p>", 400

    # Call the OSRM API with the coordinates
    route = get_osrm_route(coordinates)

    # Return the route as JSON
    return render_template('partials/route_result.html', route=route)

def get_coordinates_from_address(address):
    nominatim_url = "https://nominatim.openstreetmap.org/search"
    params = {
        'q': address,
        'format': 'json',
        'addressdetails': 1,
        'limit': 1
    }

    response = requests.get(nominatim_url, params=params,headers=headers)
    print("Address to Coordinates res ", response)

    if response.status_code == 200:
        try:
            data = response.json()
            if data:
                location_data = data[0]
                return [float(location_data['lat']), float(location_data['lon'])]
            else:
                print(f"No results found for address: {address}")
                return None
        except requests.exceptions.JSONDecodeError:
            print(f"Invalid JSON response for address: {address}")
            return None
    else:
        print(f"Error fetching data for address {address}: Status Code {response.status_code}")
        return None

def get_osrm_route(coordinates):
    coord_str = ";".join([f"{coord[1]},{coord[0]}" for coord in coordinates])
    osrm_url = f"http://router.project-osrm.org/route/v1/driving/{coord_str}?overview=full&geometries=geojson"

    response = requests.get(osrm_url)
    if response.status_code == 200:
        print("OSRM response ", response.json())
        return response.json()
    else:
        return {"error": "Unable to fetch route from OSRM"}

if __name__ == '__main__':
    app.run(debug=True)
