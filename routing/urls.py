from django.urls import path

from .views import (
    health_check,
    fuel_stations,
    fuel_data_info,
    route_api,
    route_page,
)


urlpatterns = [
    path("", route_page),
    path("health/", health_check),
    path("fuel-stations/", fuel_stations),
    path("fuel-data-info/", fuel_data_info),
    path("route/", route_api),
]