from flask import Flask
from flask import render_template
from flask import request
from config import Config
import requests

app = Flask(__name__)

def get_coordinates(location, api_key):
            url = f"http://api.openweathermap.org/geo/1.0/direct?q={location}&limit=1&appid={api_key}"
            response = requests.get(url)
            data = response.json()
            print(data)
            if data:
                return data[0]['lat'], data[0]['lon']
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
        print(location)
        print("Api key: ", Config.OPEN_MAP_API)
        latitude, longitude = get_coordinates(location, Config.OPEN_MAP_API_KEY)
        print(f"Coordinates: Latitude={latitude}, Longitude={longitude}")
        if latitude==None and longitude==None:
            return render_template('pages/error.html', error="Location not found")
        print(f"Coordinates: Latitude={latitude}, Longitude={longitude}")
        # display the locaton on the map
        return render_template('pages/map/map_layout.html', location=location)
    return render_template('pages/checkmap.html')




if __name__ == '__main__':
    app.run(debug=True)