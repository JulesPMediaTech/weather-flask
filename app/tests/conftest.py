"""
Pytest configuration file for shared fixtures.
This file is automatically discovered by pytest.
"""
import pytest
import sys
from pathlib import Path

# Add parent directory to path so we can import app modules
sys.path.insert(0, str(Path(__file__).parent.parent))

from server import app


@pytest.fixture
def client():
    """Create a test client for the Flask app."""
    app.config["TESTING"] = True
    app.config["WTF_CSRF_ENABLED"] = False  # Disable CSRF for testing
    with app.test_client() as client:
        yield client


@pytest.fixture
def app_context():
    """Create an application context for tests that need it."""
    with app.app_context():
        yield app
