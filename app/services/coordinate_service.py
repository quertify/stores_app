import requests
from typing import List, Dict, Tuple, Optional
class CoordinateService:
    def __init__(self, api_url:str) -> None:
        self.api_url = api_url

    def get_coordinates(self, postcode:str)-> Tuple[Optional[float], Optional[float]]:
        """Fetch latitude and longitude for a given postcode from Postcodes.io."""
        response = requests.get(f'{self.api_url}{postcode}')
        data = response.json()
        if response.status_code == 200 and 'result' in data:
            return data['result']['latitude'], data['result']['longitude']
        return None, None

    def get_coordinates_bulk(self,postcodes:List[str])->Dict[str, Tuple[float,float]]:
        """Fetch latitude and longitude for a list of postcodes from Postcodes.io using the bulk API."""
        if not postcodes:
            return {}
        # Split postcodes into chunks of 100 or less
        def split_list(lst: List[str], size: int)-> List[List[str]]:
            return [lst[i:i + size] for i in range(0, len(lst), size)]
        
        # Split postcodes into chunks
        chunks = split_list(postcodes, 100)
        
        coordinates = {}
        
        for chunk in chunks:
            # Prepare the request payload
            payload = {'postcodes': chunk}
            
            # Send the request
            response = requests.post(self.api_url, json=payload)
            data = response.json()
            
            if response.status_code == 200 and 'result' in data:
                for result in data['result']:
                    postcode = result['query']
                    result_data = result.get('result', {})
                    if result_data:
                        latitude = result_data.get('latitude')
                        longitude = result_data.get('longitude')
                    # Store only latitude and longitude
                        if latitude is not None and longitude is not None:
                            coordinates[postcode] = (latitude, longitude)
            else:
                print(f"Error fetching data: {data.get('error', 'Unknown error')}")
        
        return coordinates
