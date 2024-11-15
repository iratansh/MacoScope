from rest_framework.views import APIView
from keras.models import load_model
from .features import load_data
from django.http import JsonResponse
from rest_framework.response import Response
from rest_framework.decorators import api_view
import logging, asyncio, aiofiles
from .models import EconomicIndicator
import csv
from datetime import datetime
from django.db import transaction
import aiomysql
from asgiref.sync import async_to_sync
from django.http import JsonResponse
from rest_framework.decorators import api_view
import numpy as np
from .features import load_data, create_dataset
from .utils import make_forecast
from django.views.decorators.http import require_http_methods


async def get_forecast(indicator, time_steps=5, future_periods=10):
    forecast = await make_forecast(indicator, future_periods=10)
    return forecast

from django.http import JsonResponse
from asgiref.sync import async_to_sync
from rest_framework.decorators import api_view

def forecast_view(request, indicator):
    try:
        # Generate the forecast using async-to-sync wrapper
        forecast = async_to_sync(make_forecast)(indicator)
        
        if forecast is not None:
            return JsonResponse({'forecast': forecast.tolist()}, status=200)
        else:
            return JsonResponse({'error': 'No forecast data available'}, status=404)

    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)


async def load_data(table_name):
    columns = {}
    try:
        connection = await aiomysql.connect(
            host="localhost",
            port=3306,
            user="mysqluser",
            password="secret1234",
            db="forecast_db",
        )

        async with connection.cursor() as cursor:
            await cursor.execute(f"SELECT * FROM {table_name}")
            headers = [desc[0] for desc in cursor.description]

            # Initialize lists for each column
            for header in headers:
                columns[header] = []

            # Fetch the data row-by-row
            async for row in cursor:
                for header, value in zip(headers, row):
                    columns[header].append(value)

    finally:
        if connection:
            await connection.ensure_closed()  # Close connection properly

    return columns


@api_view(["POST"])
def gdp_data(request):
    logging.info("GDP data requested")

    # Use async_to_sync to call load_data asynchronously in a synchronous view
    data = async_to_sync(load_data)("gdp")

    dates = [d for d in data.get("date", [])]
    values = [float(v) for v in data.get("NGDPSAXDCCAQ", [])]

    response_data = {
        "labels": dates,
        "values": values,
        "label": "Millions of Domestic Currency, Seasonally Adjusted",
        "x_label": "Date",
        "y_label": "GDP (Millions of Domestic Currency, Seasonally Adjusted)",
    }
    return Response(response_data)


@api_view(["POST"])
def unemployment_data(request):
    logging.info("Unemployment data requested")

    # Use async_to_sync to call load_data asynchronously in a synchronous view
    data = async_to_sync(load_data)("unemployment_rate")

    provinces = [d for d in data.get("\ufeffProvince and Territories", [])]
    values = [float(v) for v in data.get("Unemployment Rates (%)", [])]

    response_data = {
        "labels": provinces,
        "values": values,
        "label": "Unemployment Rate (%)",
        "x_axis_label": "Provinces / Territories",
        "y_axis_label": "Unemployment Rate (%)",
    }
    return Response(response_data)


@api_view(["POST"])
def interest_data(request):
    logging.info("Interest data requested")
    data = async_to_sync(load_data)("interest")

    dates = [d for d in data.get("date", [])]
    values = [float(v) for v in data.get("Percent", [])]

    response_data = {
        "labels": dates,
        "values": values,
        "label": "Interest Rate (%)",
        "x_axis_label": "Date",
        "y_axis_label": "Interest Rate (%)",
    }
    return Response(response_data)


@api_view(["POST"])
def labour_data(request):
    logging.info("Labour data requested")
    data = async_to_sync(load_data)("labour")

    dates = [d for d in data.get('\ufeff"REF_DATE"', [])]
    values = [float(v) for v in data.get("VALUE", [])]

    response_data = {
        "labels": dates,
        "values": values,
        "label": "Labour force characteristics, monthly, unadjusted for seasonality (x 1,000)",
        "x_axis_label": "Date",
        "y_axis_label": "Employment Both sexes, (x 1,000)",
    }
    return Response(response_data)


@api_view(["POST"])
def exchange_data(request):
    logging.info("Exchange rate data requested")
     # Pagination parameters (e.g., from request)
    page = int(request.data.get('page', 1))
    page_size = int(request.data.get('page_size', 100))

    # Load the exchange rate data asynchronously
    data = async_to_sync(load_data)("exchange")

    # Extract the dates
    dates = [d for d in data.get('\ufeff"date"', [])]
    paginated_dates = dates[(page - 1) * page_size: page * page_size]
    

    # Prepare a list to store datasets for each currency
    datasets = []
    

    # Define colors for each currency dataset (optional)
    colors = [
        "#FF0000",  # Red
        "#00FF00",  # Green
        "#0000FF",  # Blue
        "#FFFF00",  # Yellow
        "#FF00FF",  # Magenta   
        "#00FFFF",  # Cyan
        "#FFA500",  # Orange
        "#800080",  # Purple
        "#FFC0CB",  # Pink
        "#808080",  # Gray
    ]
    color_index = 0

    # Iterate through each key in data (skipping 'date' and 'id' fields)
    for key in data.keys():
        if key not in ["id", '\ufeff"date"']:
            # Store the exchange rate values for each currency
            values = [
                float(v) if v.strip() and v.replace(".", "", 1).isdigit() else 0.0
                for v in data.get(key, [])
            ]

            paginated_values = values[(page - 1) * page_size: page * page_size]


            # Add each currency data as a separate dataset
            datasets.append(
                {
                    "label": key.replace('"', ""),  # Remove any extra quotation marks
                    "values": paginated_values,
                    "borderColor": colors[
                        color_index % len(colors)
                    ],  # Cycle through colors
                }
            )

            color_index += 1

    # Structure the response data with dates and datasets
    response_data = {
        "labels": paginated_dates,  # x-axis dates
        "datasets": datasets,  # List of currency-specific datasets
        "x_label": "Date",
        "y_label": "Exchange Rate (to CAD)",
    }

    return JsonResponse(response_data)



