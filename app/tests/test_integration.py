"""
Integration tests that test the full workflow.
"""
import pytest
from coordinates import get_coordinates
from meteo_API_response import openmeteo_data


def test_full_workflow_london():
    """Test the complete workflow: address -> coordinates -> weather data."""
    # Step 1: Get coordinates for London
    location = get_coordinates("London, UK")
    
    assert location is not None, "Failed to get coordinates for London"
    
    # Step 2: Get weather data using those coordinates
    coords = (location.latitude, location.longitude)
    response, hourly_dataframe = openmeteo_data(coords)
    
    assert response is not None, "Failed to get weather data"
    assert len(hourly_dataframe) > 0, "Weather dataframe is empty"
    
    # Step 3: Verify we can access the data
    assert 'temperature_2m' in hourly_dataframe.columns
    assert 'date' in hourly_dataframe.columns
    
    print(f"\nSuccessfully fetched weather for {location.address}")
    print(f"Coordinates: {response.Latitude()}°N {response.Longitude()}°E")
    print(f"First temperature: {hourly_dataframe['temperature_2m'].iloc[0]}°C")


def test_full_workflow_multiple_cities():
    """Test the workflow with multiple cities."""
    cities = ["Paris", "Berlin", "Madrid"]
    
    for city in cities:
        # Get coordinates
        location = get_coordinates(city)
        assert location is not None, f"Failed to get coordinates for {city}"
        
        # Get weather data
        coords = (location.latitude, location.longitude)
        response, hourly_dataframe = openmeteo_data(coords)
        
        assert response is not None, f"Failed to get weather for {city}"
        assert len(hourly_dataframe) > 0, f"No weather data for {city}"


def test_workflow_with_detailed_address():
    """Test workflow with a specific address."""
    address = "10 Downing Street, London"
    
    location = get_coordinates(address)
    
    if location:  # Address might be too specific
        coords = (location.latitude, location.longitude)
        response, hourly_dataframe = openmeteo_data(coords)
        
        assert response is not None
        assert hourly_dataframe is not None
        
        # Verify the location is in London area
        assert 51.0 < response.Latitude() < 52.0
        assert -1.0 < response.Longitude() < 0.5
