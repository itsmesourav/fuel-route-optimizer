import json

from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt

from .services.route_service import calculate_route


def route_page(request):
    return render(
        request,
        "routing/route.html"
    )

@csrf_exempt
def route_api(request):

    if request.method != "POST":
        return JsonResponse(
            {
                "error": "Only POST requests are allowed."
            },
            status=405
        )

    try:

        body = json.loads(
            request.body
        )

        start = body.get("start")
        finish = body.get("finish")

        if not start or not finish:

            return JsonResponse(
                {
                    "error": (
                        "Both 'start' and "
                        "'finish' are required."
                    )
                },
                status=400
            )

        result = calculate_route(
            start,
            finish
        )

        return JsonResponse(
            result,
            status=200
        )

    except json.JSONDecodeError:

        return JsonResponse(
            {
                "error": "Invalid JSON body."
            },
            status=400
        )

    except ValueError as error:

        return JsonResponse(
            {
                "error": str(error)
            },
            status=400
        )

    except Exception as error:

        return JsonResponse(
            {
                "error": (
                    "Unable to calculate route.",
                    str(error)
                )
            },
            status=500
        )


def health_check(request):
    return JsonResponse({
        "status": "ok",
        "message": "Fuel Route Optimizer API is running"
    })


def fuel_stations(request):
    df = load_fuel_stations()

    stations = df.head(10).to_dict(orient="records")

    return JsonResponse({
        "total_stations": len(df),
        "stations": stations
    })


def fuel_data_info(request):
    df = load_fuel_stations()

    return JsonResponse({
        "total_rows": len(df),
        "columns": list(df.columns),
        "states": sorted(df["State"].unique().tolist()),
        "unique_cities": int(df["City"].nunique())
    })