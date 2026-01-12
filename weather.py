from dotenv import load_dotenv
from pprint import pprint
import requests
import os

load_dotenv()

def get_current_weather(city="London"):
    '''
  Deprecated MetOffice datapoint service
    '''
    resource = 'val/wxfcs/all/json/sitelist'
    # timescale = 'res=3hourly&'
    timescale = ''
    request_url = f'http://datapoint.metoffice.gov.uk/public/data/{resource}?{timescale}key={os.getenv("MET_KEY")}'
    print (request_url)

    weather_data = requests.get(request_url)
    return weather_data


if __name__ == "__main__":
    print ("\n*** Get weather info ***\n")
    site = input ("Enter site or location: ")
    weather_data = get_current_weather(site)
    pprint(weather_data)
