"""
Tests for the meteo_API_response module.
"""
import pytest
import pandas as pd
from meteo_API_response import openmeteo_data


def test_openmeteo_data_valid_coordinates():
    """Test fetching weather data for valid coordinates."""
    # London coordinates
    coords = (51.5074, -0.1278)
    
    response, hourly_dataframe = openmeteo_data(coords)
    
    # Check response object has expected methods
    assert response is not None
    assert hasattr(response, 'Latitude')
    assert hasattr(response, 'Longitude')
    assert hasattr(response, 'Elevation')
    
    # Check coordinates match (approximately)
    assert abs(response.Latitude() - coords[0]) < 1.0
    assert abs(response.Longitude() - coords[1]) < 1.0
    
    # Check dataframe structure
    assert isinstance(hourly_dataframe, pd.DataFrame)
    assert 'date' in hourly_dataframe.columns
    assert 'temperature_2m' in hourly_dataframe.columns
    assert len(hourly_dataframe) > 0


def test_openmeteo_data_paris():
    """Test fetching weather data for Paris."""
    # Paris coordinates
    coords = (48.8566, 2.3522)
    
    response, hourly_dataframe = openmeteo_data(coords)
    
    assert response is not None
    assert isinstance(hourly_dataframe, pd.DataFrame)
    
    # Check we got temperature data
    assert not hourly_dataframe['temperature_2m'].isna().all()
    
    # Temperature should be reasonable (between -50 and 50 Celsius)
    temps = hourly_dataframe['temperature_2m']
    assert temps.min() > -50
    assert temps.max() < 50


def test_openmeteo_data_extreme_north():
    """Test fetching weather data for northern coordinates."""
    # Reykjavik, Iceland
    coords = (64.1466, -21.9426)
    
    response, hourly_dataframe = openmeteo_data(coords)
    
    assert response is not None
    assert isinstance(hourly_dataframe, pd.DataFrame)
    assert len(hourly_dataframe) > 0


def test_openmeteo_dataframe_types():
    """Test that the dataframe has correct data types."""
    coords = (51.5, -0.1)
    
    response, hourly_dataframe = openmeteo_data(coords)
    
    # Check date column is datetime
    assert pd.api.types.is_datetime64_any_dtype(hourly_dataframe['date'])
    
    # Check temperature is numeric
    assert pd.api.types.is_numeric_dtype(hourly_dataframe['temperature_2m'])


def test_openmeteo_data_returns_tuple():
    """Test that the function returns a tuple of two elements."""
    coords = (40.7128, -74.0060)  # New York
    
    result = openmeteo_data(coords)
    
    assert isinstance(result, tuple)
    assert len(result) == 2
