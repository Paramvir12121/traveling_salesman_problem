from flask import Flask
from flask import render_template
from flask import request
from config import Config
import requests

app = Flask(__name__)

 


def get_coordinates(location):
    url = "https://nominatim.openstreetmap.org/search"
    params = {
        "q": location.strip(),
        "format": "json",
        "addressdetails": 1,
        "limit": 1,
    }

    headers = {'User-Agent': Config.OSM_HEADER}
    
    try:
        response = requests.get(url, params=params,headers=headers, timeout=10)
        response.raise_for_status()  # Raise an HTTPError for bad responses (4xx and 5xx)
        
        # Check if the response contains valid JSON
        if response.headers.get("Content-Type") == "application/json":
            data = response.json()
            if data:
                return data[0]['lat'], data[0]['lon']
            else:
                return None, None
        else:
            print(f"Unexpected response type: {response.headers.get('Content-Type')}")
            print(f"Response text: {response.text}")
    except requests.exceptions.RequestException as e:
        print(f"Error fetching data from the API: {e}")
    except (ValueError, KeyError) as e:
        print(f"Error parsing response JSON: {e}")
    
    return None, None


@app.route('/')
def home():
    return render_template('pages/home.html')

@app.route('/about')
def about():
    return render_template('pages/about.html')

@app.route('/test')
def test():
    return render_template('pages/test.html')

@app.route('/services')
def services():
    return render_template('pages/services.html')

@app.route('/contact', methods=['GET', 'POST'])
def contact():
    if request.method == 'POST':
        name = request.form['name']
        print(name)
        email = request.form['email']
        print(email)
        message = request.form['message']
        print(message)
        with open('contacted.txt', 'a') as file:
            file.write(f"Name: {name}\n")
            file.write(f"Email: {email}\n")
            file.write(f"Message: {message}\n")
            file.write("\n")
        return render_template('pages/home.html')
    return render_template('pages/contact.html')



@app.route('/checkmap', methods=['GET', 'POST'])
def checkmap():
    if request.method == 'POST':
        location = request.form['location']
        location = location.strip()
        if not location:
            return render_template('pages/error.html', error="Invalid location")
        print(location)
        latitude, longitude = get_coordinates(location)
        print(f"Coordinates: Latitude={latitude}, Longitude={longitude}")
        if not latitude or not longitude:
            return render_template('pages/error.html', error="Location not found")
        print(f"Coordinates: Latitude={latitude}, Longitude={longitude}")
        # display the locaton on the map
        return render_template('pages/map/test_map.html', location=location, latitude=latitude, longitude=longitude)
    return render_template('pages/checkmap.html')




if __name__ == '__main__':
    app.run(debug=True)