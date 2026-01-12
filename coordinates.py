from geopy.geocoders import Nominatim
from pprint import pprint

def get_coordinates(my_address):
    geolocator = Nominatim(user_agent='coordinator')
    location = geolocator.geocode(my_address)
    return location

if __name__ == "__main__":
    print ('''
*** Longitude and Latitude finder ***
           ''')
    my_address = None
    while not my_address:
        my_address = input ("Enter address here: ")
    loc = get_coordinates(my_address)
    pprint(f'{loc.address} : Longitude: {loc.longitude} Latitude: {loc.latitude}')


