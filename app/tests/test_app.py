"""
Tests for Flask routes and endpoints.
"""
import pytest


def test_index_route(client):
    """Test the index route returns 200 and shows the expected content."""
    response = client.get("/")
    assert response.status_code == 200
    assert b"Coordinates" in response.data or b"Enter" in response.data


def test_index_route_with_status(client):
    """Test the index route handles status query parameters."""
    response = client.get("/?status=test_error")
    assert response.status_code == 200


def test_coordinates_route_no_address(client):
    """Test coordinates route without address parameter."""
    response = client.get("/coordinates")
    assert response.status_code in (200, 302)  # Should redirect or handle gracefully


def test_coordinates_route_with_invalid_address(client):
    """Test coordinates route with invalid address redirects to index."""
    response = client.get("/coordinates?address=InvalidXYZ123456789")
    # Should redirect back to index with error status
    assert response.status_code in (200, 302)


def test_coordinates_route_with_valid_address(client):
    """Test coordinates route with a valid address."""
    response = client.get("/coordinates?address=London")
    # Should return 200 with coordinates page
    assert response.status_code == 200
    if response.status_code == 200:
        assert b"Longitude" in response.data or b"Latitude" in response.data
