from flask import Blueprint, render_template, request, jsonify
from app.services.store_service import StoreService
from app.services.coordinate_service import CoordinateService
from math import ceil
from app.config import Config

main = Blueprint('main', __name__)


store_file = Config.STORES_FILE
api_url = Config.POSTCODES_API_URL

@main.route('/')
def index():
    """Render the index page with a list of stores sorted by name, including their coordinates."""

    store_service = StoreService(store_file , api_url)
    coordinate_service = CoordinateService(api_url)
    
    # Load stores from the service
    stores = store_service.get_stores()
    
    # List postcodes from stores
    postcodes = [store['postcode'] for store in stores]
    
    # Get coordinates for all postcodes in bulk
    coords = coordinate_service.get_coordinates_bulk(postcodes)
    
    # Add coordinates to store data
    stores_with_coords = []
    for store in stores:
        postcode = store['postcode']
        latitude, longitude = coords.get(postcode, (None, None))
        store_with_coord = {
            'name': store['name'],
            'postcode':store['postcode'],
            'latitude': latitude,
            'longitude': longitude
        }
        stores_with_coords.append(store_with_coord)
    
    # Sort stores by name and using inplace sort for it
    stores_with_coords.sort(key=lambda x: x['name'])
    
    # Render template with sorted stores
    return render_template('index.html', stores=stores_with_coords)

@main.route('/stores_in_radius', methods=['GET'])
def stores_in_radius():
    """Return stores within a specified radius from a given postcode, with pagination."""
    
    store_service = StoreService(store_file , api_url)
    postcode = request.args.get('postcode')
    radius_str = request.args.get('radius')
    page_str = request.args.get('page', 1)  # Default to page 1 
    page_size_str = request.args.get('page_size', 10)  # Default to 10 stores per page
    
    # Validate postcode and radius
    if not postcode or not radius_str:
        return jsonify({"Error": "Missing postcode or radius parameter"}), 400

    try:
        radius = float(radius_str)
    except ValueError:
        return jsonify({"Error": "Invalid radius value. It must be a number."}), 400
    
    try:
        page = int(page_str)
        page_size = int(page_size_str)
    except ValueError:
        return jsonify({"Error": "Invalid page or page_size value. They must be integers."}), 400
    
    if page < 1 or page_size < 1:
        return jsonify({"Error": "Page and page_size must be greater than 0."}), 400

    # Get stores within the radius
    stores = store_service.get_stores_in_radius(postcode, radius)

    # Pagination 
    total_stores = len(stores)
    total_pages = ceil(total_stores / page_size)
    start = (page - 1) * page_size
    end = start + page_size

    paginated_stores = stores[start:end]

    # Return paginated results and store data
    return jsonify({
        "stores": paginated_stores,
        "page": page,
        "page_size": page_size,
        "total_stores": total_stores,
        "total_pages": total_pages
    })
