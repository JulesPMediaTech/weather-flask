"""
Tests for the coordinates module.
"""
import pytest
from coordinates import get_coordinates


def test_get_coordinates_valid_address():
    """Test geocoding a well-known location."""
    location = get_coordinates("London")
    
    assert location is not None
    assert location.latitude is not None
    assert location.longitude is not None
    assert location.address is not None
    
    # London coordinates are roughly (51.5, -0.1)
    assert 51.0 < location.latitude < 52.0
    assert -1.0 < location.longitude < 0.5


def test_get_coordinates_specific_address():
    """Test geocoding a specific address."""
    location = get_coordinates("Eiffel Tower, Paris")
    
    assert location is not None
    assert "Paris" in location.address or "Eiffel" in location.address
    
    # Eiffel Tower coordinates are roughly (48.86, 2.29)
    assert 48.0 < location.latitude < 49.0
    assert 2.0 < location.longitude < 3.0


def test_get_coordinates_invalid_address():
    """Test geocoding with an invalid address returns None."""
    location = get_coordinates("XYZ123InvalidAddressThatDoesNotExist456789")
    
    # Nominatim returns None for addresses it cannot find
    assert location is None


def test_get_coordinates_empty_string():
    """Test geocoding with an empty string."""
    location = get_coordinates("")
    
    # Should return None or handle gracefully
    assert location is None


def test_get_coordinates_coordinates_format():
    """Test that coordinates can be used with lat/long format."""
    location = get_coordinates("New York")
    
    if location:
        # Test that we can use these coordinates
        assert isinstance(location.latitude, float)
        assert isinstance(location.longitude, float)
        assert -90 <= location.latitude <= 90
        assert -180 <= location.longitude <= 180
