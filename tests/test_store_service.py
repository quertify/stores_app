import unittest
import pytest
from unittest.mock import patch, MagicMock
from app.services.store_service import StoreService

@pytest.fixture
def mock_stores_file():
    return '[{"name": "Store 1", "postcode": "E15 2SR"}]'

@pytest.fixture
def mock_coordinate_service():
    mock = MagicMock()
    mock.get_coordinates_bulk.return_value = {'E15 2SR': (51.5074, -0.1278)}
    mock.get_coordinates.return_value = (51.5074, -0.1278)
    return mock

@pytest.fixture
def store_service(mock_stores_file, mock_coordinate_service):
    with patch('builtins.open', new_callable=unittest.mock.mock_open, read_data=mock_stores_file):
        service = StoreService('dummy_stores.json','https://fake/api')
        service.coordinate_service = mock_coordinate_service
        return service


def test_get_store_coordinates(store_service, mock_coordinate_service):
    stores = [{'name': 'Store 1', 'postcode': 'E15 2SR'}]
    coordinates = store_service.get_store_coordinates(stores)
    assert coordinates == {'E15 2SR': (51.5074, -0.1278)}
    mock_coordinate_service.get_coordinates_bulk.assert_called_once_with(['E15 2SR'])

@patch('app.services.store_service.calculate_distance')
def test_filter_stores_by_radius(mock_calculate_distance, store_service):
    mock_calculate_distance.return_value = 5.0
    stores = [{'name': 'Store 1', 'postcode': 'E15 2SR'}]
    filtered_stores = store_service.filter_stores_by_radius(stores, 51.5074, -0.1278, 10)
    expected_stores = [
        {'name': 'Store 1', 'postcode': 'E15 2SR', 'latitude': 51.5074, 'longitude': -0.1278, 'distance': 5.0}
    ]
    assert filtered_stores == expected_stores

def test_sort_stores_north_to_south(store_service):
    stores = [
        {'name': 'Store 1', 'latitude': 51.5074},
        {'name': 'Store 2', 'latitude': 48.8566}
    ]
    sorted_stores = store_service.sort_stores_north_to_south(stores)
    assert sorted_stores == [
        {'name': 'Store 1', 'latitude': 51.5074},
        {'name': 'Store 2', 'latitude': 48.8566}
    ]

def test_get_stores_in_radius(store_service):
    with patch.object(store_service, 'filter_stores_by_radius') as mock_filter:
        mock_filter.return_value = [{'name': 'Store 1', 'postcode': 'E15 2SR', 'latitude': 51.5074, 'longitude': -0.1278, 'distance': 5.0}]
        stores = store_service.get_stores_in_radius('AB1 2CD', 10)
        assert stores == [{'name': 'Store 1', 'postcode': 'E15 2SR', 'latitude': 51.5074, 'longitude': -0.1278, 'distance': 5.0}]