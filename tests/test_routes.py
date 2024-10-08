import pytest
from flask import json
from app import create_app
from unittest.mock import patch
# Fixture to create a test client
@pytest.fixture
def client():
    app = create_app()
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

# Fixture to mock StoreService
@pytest.fixture
def mock_store_service():
    with patch('app.routes.store_routes.StoreService') as MockStoreService:
        yield MockStoreService.return_value

# Fixture to mock CoordinateService which we created in routes.py
@pytest.fixture
def mock_coordinate_service():
    with patch('app.routes.store_routes.CoordinateService') as MockCoordinateService:
        yield MockCoordinateService.return_value

def test_index(client, mock_store_service, mock_coordinate_service):
    mock_store_service.get_stores.return_value = [{'name': 'Store 1', 'postcode': 'AB1 2CD'}]
    mock_coordinate_service.get_coordinates_bulk.return_value = {'AB1 2CD': (51.5074, -0.1278)}

    response = client.get('/')
    assert response.status_code == 200
    data = response.data.decode()
    assert 'Store 1' in data
    assert '51.5074' in data
    assert '-0.1278' in data

def test_stores_in_radius(client, mock_store_service):
    mock_store_service.get_stores_in_radius.return_value = [
        {'name': 'Store 1', 'postcode': 'AB1 2CD', 'latitude': 51.5074, 'longitude': -0.1278, 'distance': 5.0}
    ]
    
    response = client.get('/stores_in_radius', query_string={'postcode': 'AB1 2CD', 'radius': 10, 'page': 1, 'page_size': 1})
    assert response.status_code == 200
    data = json.loads(response.data)
    
    expected_data = {
        "stores": [{'name': 'Store 1', 'postcode': 'AB1 2CD', 'latitude': 51.5074, 'longitude': -0.1278, 'distance': 5.0}],
        "page": 1,
        "page_size": 1,
        "total_stores": 1,
        "total_pages": 1
    }
    assert data == expected_data

#  To test the missing parameter
def test_stores_in_radius_missing_params(client):
    response = client.get('/stores_in_radius', query_string={'postcode': 'AB1 2CD'})
    assert response.status_code == 400
    data = json.loads(response.data)
    assert data['Error'] == "Missing postcode or radius parameter"

# To test the invalid radius
def test_stores_in_radius_invalid_radius(client):
    response = client.get('/stores_in_radius', query_string={'postcode': 'AB1 2CD', 'radius': 'invalid'})
    assert response.status_code == 400
    data = json.loads(response.data)
    assert data['Error'] == "Invalid radius value. It must be a number."
