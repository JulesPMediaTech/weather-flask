import openmeteo_requests

import pandas as pd
import requests_cache
from retry_requests import retry

def openmeteo_data(coords):
    # Setup the Open-Meteo API client with cache and retry on error
    cache_session = requests_cache.CachedSession('.cache', expire_after = 3600)
    retry_session = retry(cache_session, retries = 5, backoff_factor = 0.2)
    openmeteo = openmeteo_requests.Client(session = retry_session)

    # Make sure all required weather variables are listed here
    # The order of variables in hourly or daily is important to assign them correctly below
    url = "https://api.open-meteo.com/v1/forecast"
    lati, longi = coords
    params = {
        "latitude": lati,
        "longitude": longi,
        "hourly": "temperature_2m",
        "models": "icon_seamless",
    }
    responses = openmeteo.weather_api(url, params=params)

    # Process first location. Add a for-loop for multiple locations or weather models
    response = responses[0]

    # Process hourly data. The order of variables needs to be the same as requested.
    hourly = response.Hourly()
    hourly_temperature_2m = hourly.Variables(0).ValuesAsNumpy()

    hourly_data = {"date": pd.date_range(
        start = pd.to_datetime(hourly.Time(), unit = "s", utc = True),
        end =  pd.to_datetime(hourly.TimeEnd(), unit = "s", utc = True),
        freq = pd.Timedelta(seconds = hourly.Interval()),
        inclusive = "left"
    )}

    hourly_data["temperature_2m"] = hourly_temperature_2m

    hourly_dataframe = pd.DataFrame(data = hourly_data)
    return response, hourly_dataframe

if __name__ == "__main__":
    coords = 51.5122, -0.302
    response, hourly_dataframe = openmeteo_data(coords)

    print(f"Coordinates: {response.Latitude()}°N {response.Longitude()}°E")
    print(f"Elevation: {response.Elevation()} m asl")
    print(f"Timezone difference to GMT+0: {response.UtcOffsetSeconds()}s")

    print("\nMethods available on response:")
    print([method for method in dir(response) if not method.startswith('_')])

    print("\nHourly data\n", hourly_dataframe)

'''
To display a pandas DataFrame as an HTML table in a Flask template (like your coordinates.html),
 use the to_html() method on the DataFrame object. Since Jinja2 auto-escapes HTML output, 
 pipe it through the safe filter to prevent escaping.

I've updated your template accordingly. 
The DataFrame (meteo_data) will now render as a proper HTML table when the page loads.

If you need to customize the table (e.g., add classes, limit rows, or style it), 
you can pass parameters to to_html(), like {{ meteo_data.to_html(classes='table table-striped') | safe }} (assuming Bootstrap or similar CSS).
'''
