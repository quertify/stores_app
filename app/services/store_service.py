import json
from typing import List, Dict, Tuple, Optional
from ..utils import  calculate_distance
from app.services.coordinate_service import CoordinateService

class StoreService:
    def __init__(self, stores_file: str, api_url:str):
        self.stores_file = stores_file
        self.coordinate_service = CoordinateService(api_url)

    def get_stores(self) -> List[Dict[str, str]]:
        """Load store data from JSON file."""
        try:
            with open(self.stores_file, 'r') as file:
                return json.load(file)
        except (FileNotFoundError, json.JSONDecodeError) as e:
            print(f"Error reading stores file: {e}")
            return []

    def get_store_coordinates(self, stores: List[Dict[str, str]]) -> Dict[str, Tuple[Optional[float], Optional[float]]]:
        """Get coordinates for a list of store postcodes using a bulk API request."""
        store_postcodes = [store['postcode'] for store in stores]
        return self.coordinate_service.get_coordinates_bulk(store_postcodes)

    def filter_stores_by_radius(self, stores: List[Dict[str, str]], lat: float, lon: float, radius: float) -> List[Dict[str, str]]:
        """Filter stores based on distance from a given location (latitude, longitude)."""
        filtered_stores = []
        store_coords = self.get_store_coordinates(stores)

        for store in stores:
            store_lat, store_lon = store_coords.get(store['postcode'], (None, None))
            
            if store_lat is None or store_lon is None:
                continue

            distance = calculate_distance(lat, lon, store_lat, store_lon)
            if distance <= radius:
                store['latitude'] = store_lat
                store['longitude'] = store_lon
                store['distance'] = round(distance, 2)
                filtered_stores.append(store)

        return filtered_stores

    def sort_stores_north_to_south(self, stores: List[Dict[str, str]]) -> List[Dict[str, str]]:
        """Sort stores from north to south based on latitude."""
        return sorted(stores, key=lambda x: x.get('latitude', 0), reverse=True)

    def get_stores_in_radius(self, postcode: str, radius: float) -> List[Dict[str, str]]:
        """
        return: A list of stores sorted from north to south.
        """
        lat, lon = self.coordinate_service.get_coordinates(postcode)

        if lat is None or lon is None:
            print(f"Coordinates for postcode {postcode} not found.")
            return []

        stores = self.get_stores()

        # Filter stores within the radius
        stores_in_radius = self.filter_stores_by_radius(stores, lat, lon, radius)

        # Sort stores from north to south
        sorted_stores = self.sort_stores_north_to_south(stores_in_radius)

        return sorted_stores
