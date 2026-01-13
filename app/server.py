from flask import Flask, render_template, request
from waitress import serve
from coordinates import get_coordinates
from meteo_API_response import openmeteo_data


app = Flask(__name__)
print ('Running Coordinates Server...')

@app.route('/')

@app.route('/index')
def index():
    status = request.args.get('status', '')
    return render_template('index.html', status=status)

@app.route('/coordinates')
def coordinates():
    my_address = request.args.get('address')
    print (my_address)
    loc = get_coordinates(my_address)

    if loc is None:
        # Prevent rendering coordinates page; redirect to index with error
        from flask import redirect, url_for
        return redirect(url_for('index', status='Coordinates not found for the address'))
    else:
    # get weather data
        response, hourly_dataframe = openmeteo_data((loc.latitude, loc.longitude))

        print(f"Coordinates: {response.Latitude()}°N {response.Longitude()}°E")
        print(f"Elevation: {response.Elevation()} m asl")
        print(f"Timezone difference to GMT+0: {response.UtcOffsetSeconds()}s")
        print("\nHourly data\n", hourly_dataframe)


        return render_template(
            'coordinates.html', 
            address = loc.address,
            longitude = loc.longitude,
            latitude = loc.latitude,
            meteo_response = response,
            meteo_data = hourly_dataframe
        )

if __name__ == '__main__':
    app.run(host='0.0.0.0',port=8000,debug=True)
    # serve(app, host='0.0.0.0',port=8000)