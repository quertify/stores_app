# Stores_app

## Project Description

This project is a Flask-based backend application designed to handle tasks 
1. Displaying a list of stores with coordinates.
2. RESTful API endpoint fetching the list of stores located in the given radius of your provided postcode

## Features

- **Index Page**: Displays a list of stores with their coordinates.
- **Stores in Radius**: Fetches stores within a specified radius from a given postcode, with pagination support.

## Requirements
- Docker
- Python 3.12
- Flask
- Additional Python packages listed in `requirements.txt`

## How to Run
Follow these steps: 
1. Download and Unzip the Application
   - Download the zip file containing the `stores_app` application.
   - Unzip the downloaded file to a directory on your local machine.
2. Navigate to the Application folder
    ``` cd path/stores_app```
3. Build the Docker Image of the application
   ```docker build -t stores_app .```
   ```docker run -d -p 5000:5000 --name stores_app_container stores_app```
4. Navigate to http://localhost:5000
5. You can also try hitting the api endpoint for stores_in_radius

## To stop the container:
```
docker stop stores_app_container
docker rm stores_app_container
```


## API Documentation

### Overview

This project provides two main API endpoints:

1. **Index Page**: Displays a sorted list of stores with their coordinates.
2. **Stores in Radius**: Retrieves stores within a specified radius from a given postcode, with pagination support.

### 1. `GET /`

#### Description

Renders the index page displaying a sorted list of stores. Each store includes its name, postcode, latitude, and longitude.

#### Implementation Details

- **Dependencies**: 
  - `StoreService` to retrieve store data from `stores.json`.
  - `CoordinateService` to fetch coordinates for each postcode using the Postcodes.io API.

#### Response

- **Status Code**: `200 OK`
- **Content-Type**: `text/html`
- **Body**: An HTML page rendered from the `index.html` template, displaying stores with their names, postcodes, and coordinates.

#### Example

A  webpage showing a list of stores

```html
<!DOCTYPE html>
<html>
<head>
    <title>Stores</title>
</head>
<body>
    <h1>Stores List</h1>
    <ul>
        <li>Store 1 - E16 2HJ - Latitude: 51.5074, Longitude: -0.1234</li>
        ...
    </ul>
</body>
</html>
```

### 2. `GET /stores_in_radius`

### Description

Returns a JSON response with a list of stores within a specified radius from a given postcode. Results are paginated and Sorted from North to South

### Query Parameters

- **postcode** (string, required): The postcode to use as the center for the search.
- **radius** (float, required): The search radius in kilometers.
- **page** (integer, optional): The page number to retrieve. Default is `1`.
- **page_size** (integer, optional): Number of stores per page. Default is `10`.

### Implementation Details

- **Validation**: Ensures that `postcode` and `radius` are provided and valid. The `radius` must be a numeric value; `page` and `page_size` must be positive integers.

### Response

- **Status Code**: 
  - `200 OK` for successful responses.
  - `400 Bad Request` for validation errors.
- **Content-Type**: `application/json`
- **Body**: A JSON object containing:
  - `stores`: An array of stores within the specified radius.
  - `page`: The current page number.
  - `page_size`: The number of stores per page.
  - `total_stores`: The total number of stores within the radius.
  - `total_pages`: The total number of pages available.

### Example

**Request:**

```http
GET /stores_in_radius?postcode=E16 1BP&radius=3page=1&page_size=5
```

**Response**
{
    "page": 1,
    "page_size": 10,
    "stores": [
        {
            "distance": 2.18,
            "latitude": 51.488666,
            "longitude": 0.020724,
            "name": "Charlton",
            "postcode": "SE7 7TZ"
        }
    ],
    "total_pages": 1,
    "total_stores": 1
}

## Folder Structure:
```
store_app/
├── app/
│   ├── __init__.py
│   └── routes/
│   |   └── store_routes.py
│   ├── services/
│   │   ├── coordinate_service.py
│   │   └── store_service.py
│   ├── utils.py
│   ├── Config.py
│   └── templates/
│       └── index.html
├── tests/
│   ├── test_store_service.py
│   └── test_routes.py
├── run.py
└── requirements.txt
├── data/
│   └── stores.json
└── README.md
└── Dockerfile
└── .dockerignore
└── Submission.md

```
### Architecture Design Concerns
1. I have used Separation of concerns principle of design while structuring this application.
2. Also implemented OOP programming so that it is more modularized and maintainable.

