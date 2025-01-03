from flask import Flask
from flask import render_template
from flask import request
from config import Config
import requests
from map_functions import get_coordinates, optimal_route


app = Flask(__name__)

 





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
        latitude, longitude, error = get_coordinates(location)
        if error:
            return render_template('pages/error.html', error=error)
        
        if not latitude or not longitude:
            return render_template('pages/error.html', error="Location not found")
        print(f"Coordinates: Latitude={latitude}, Longitude={longitude}")
        # display the locaton on the map
        return render_template('pages/map/map_layout.html', location=location, latitude=latitude, longitude=longitude)
    return render_template('pages/forms/checkmap.html')



@app.route('/checkroute', methods=['GET', 'POST'])
def checkroute():
    if request.method == 'POST':
        routes = request.form.getlist('locations')
        print("routes",routes)
        if not routes:
            return render_template('pages/error.html', error="Invalid routes")
        visit_sequence = optimal_route(routes)
        print(visit_sequence)
    return render_template('pages/forms/checkroutesform.html')


@app.route('/add-location')
def add_location():
    return '<input type="text" name="locations" placeholder="Enter your location">'  



if __name__ == '__main__':
    app.run(debug=True)