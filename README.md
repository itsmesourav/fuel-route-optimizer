# Fuel Route Optimizer

A Django-based API and web application that calculates a driving route between two locations in the USA and recommends cost-effective fuel stops along the route.

The application considers a vehicle with a maximum range of 500 miles and fuel efficiency of 10 MPG. It uses the provided fuel-price dataset to select fuel stops while minimizing the overall fuel cost.

## Features

- Route calculation between two USA locations
- Interactive route map
- Fuel station data from the provided CSV dataset
- Fuel station coordinates for map visualization
- Fuel price comparison along the route
- Cost-effective fuel stop optimization
- 500-mile maximum vehicle range
- 50-gallon maximum fuel capacity
- 10 MPG fuel efficiency
- Total gallons purchased calculation
- Total fuel cost calculation
- Multiple fuel stops for long-distance routes
- API validation for missing or invalid locations
- Interactive web interface
- Postman-compatible REST API

## Technology Stack

- Python 3.14+
- Django 6.1
- Django REST Framework
- Pandas
- NumPy
- SciPy
- Requests
- JavaScript
- Leaflet
- OpenStreetMap
- OSRM Routing API
- SQLite for local Django development

## Project Structure

```text
fuel-route-optimizer/
│
├── fuel_route/
│   ├── settings.py
│   ├── urls.py
│   ├── asgi.py
│   └── wsgi.py
│
├── routing/
│   ├── data/
│   │   ├── fuel-prices.csv
│   │   └── fuel-stations.csv
│   │
│   ├── services/
│   │   ├── fuel_optimizer.py
│   │   ├── geocoding.py
│   │   ├── route_service.py
│   │   └── station_finder.py
│   │
│   ├── templates/
│   │   └── routing/
│   │       └── route.html
│   │
│   ├── fuel_data.py
│   ├── views.py
│   └── urls.py
│
├── scripts/
│   └── prepare_stations.py
│
├── test_optimizer.py
├── test_routing.py
├── test_station_finder.py
├── manage.py
├── requirements.txt
└── .gitignore
