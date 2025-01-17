from flask import Flask
from flask import render_template
from flask import request
from config import Config
import requests
from map_functions import get_coordinates, optimal_route, get_route,nearest_neighbour, plot_route


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
        return render_template('map/map_layout.html', location=location, latitude=latitude, longitude=longitude)
    return render_template('forms/checkmap.html')


@app.route('/checkoneroute', methods=['GET', 'POST'])
def checkoneroute():
    if request.method == 'POST':
        start_location = request.form['start_location']
        end_location = request.form['end_location']
        print("start location", start_location, "end location", end_location)
        if not start_location and not end_location:
            return render_template('pages/error.html', error="Invalid location")
        start_location = start_location.strip()
        end_location = end_location.strip()
        start_lat, start_long, start_cord_error = get_coordinates(
            start_location)
        end_lat, end_long, end_cord_error = get_coordinates(end_location)
        start_coordinates = [start_lat, start_long]
        end_coordinates = [end_lat, end_long]

        if not start_coordinates or not end_coordinates:
            if start_cord_error and end_cord_error:
                error_message = start_cord_error + " and " + end_cord_error
                return render_template('pages/error.html', error=error_message)
            elif start_cord_error:
                return render_template('pages/error.html', error=start_cord_error)
            elif end_cord_error:
                return render_template('pages/error.html', error=end_cord_error)
            return render_template('pages/error.html', error="Location not found")
        print("Start coordinates: ", start_coordinates,
              "End coordinates: ", end_coordinates)
        route = get_route([start_coordinates, end_coordinates])
        print("Route: ", route)
        # display the locaton on the map
        return render_template('map/one_route_map.html', start_location=start_location, end_location=end_location, start_coordinates=start_coordinates, end_coordinates=end_coordinates, route=route)
        # return render_template('pages/map/map_layout.html', start_location=start_location, end_location=end_location)
    return render_template('forms/onerouteform.html')


@app.route('/nearestnightbour', methods=['GET', 'POST'])
def nearestnightbour():
    if request.method == 'POST':
        location = request.form.getlist('locations')
        print("location", location)
        if not location:
            return render_template('pages/error.html', error="Invalid location")
        location_coordinates = []
        for loc in location:
            loc = loc.strip()
            if not loc:
                return render_template('pages/error.html', error="Invalid location")
            print(loc)
            latitude, longitude, error = get_coordinates(loc)
            if error:
                return render_template('pages/error.html', error=error)
            if not latitude or not longitude:
                return render_template('pages/error.html',error=f"Location '{loc}' not found")
            location_coordinates.append([latitude, latitude, loc])
            print(f"Coordinates: Latitude={latitude}, Longitude={longitude}")
        print("all location Coordiantes: ", location_coordinates)
        route,error = nearest_neighbour(location_coordinates)
        print("Route: ", route)
        if error:
            return render_template('pages/error.html', error=error)
        final_route = []
        final_route = plot_route(route)
        print("Final Route: ", final_route)
        return render_template('map/nearest_neighbour_route.html', location=location, route=final_route)
        # display the locaton on the map

    return render_template('forms/nearestneighbourform.html')


@app.route('/add-location')
def add_location():
    return '<input type="text" name="locations" placeholder="Enter your location">'


if __name__ == '__main__':
    app.run(debug=True)
