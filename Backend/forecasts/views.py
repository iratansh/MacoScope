"""
This file contains the views for the forecast API
"""

from .features import load_data
from django.http import JsonResponse
from rest_framework.response import Response
from rest_framework.decorators import api_view
import logging
import aiomysql
from asgiref.sync import async_to_sync
from django.http import JsonResponse
from rest_framework.decorators import api_view
from .features import load_data
from .utils import make_forecast

async def get_forecast(indicator, time_steps=5, future_periods=10):
    """
    Get a forecast for a specific indicator
    """
    forecast = await make_forecast(indicator, future_periods=10)
    return forecast

def forecast_view(request, indicator):
    """
    API view to generate a forecast for a specific economic indicator

    Args:
        request (django.http.HttpRequest): The request object
        indicator (str): The economic indicator to generate the forecast for

    Returns:
        django.http.JsonResponse: The forecast data as a JSON response
    """
    try:
        # Generate the forecast using async-to-sync wrapper
        forecast = async_to_sync(make_forecast)(indicator)

        if forecast is not None:
            return JsonResponse({"forecast": forecast.tolist()}, status=200)
        else:
            return JsonResponse({"error": "No forecast data available"}, status=404)

    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)


async def load_data(table_name):
    """
    Load historical economic data from the MySQL database asynchronously.

    Parameters:
    - table_name: The name of the database table to load from.

    Returns:
    - columns: A dictionary with column names as keys and lists of values as values.
    """
    columns = {}

    connection = await aiomysql.connect(
        host="db3",
        port=3306,
        user="mysqluser",
        password="secret1234",
        db="forecast_db",
    )
    try:
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
    """
    Return historical GDP data in response to a POST request.

    Returns:
    - response_data: A dictionary containing the dates and values of the GDP data.
    """
    logging.info("GDP data requested")

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
    """
    Return unemployment rate data in response to a POST request.

    Returns:
    - response_data: A dictionary containing the province / territory names and
      unemployment rates.
    """
    logging.info("Unemployment data requested")

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
    """
    Return interest rate data in response to a POST request.

    Returns:
    - response_data: A dictionary containing the interest rate data.
    """
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
    """
    Return labour data in response to a POST request.

    Returns:
    - response_data: A dictionary containing the labour data.
    """
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
    """
    Return exchange rate data in response to a POST request.

    The request data should contain pagination parameters:
    - page (int): The page number to return (default: 1).
    - page_size (int): The number of items per page (default: 100).

    Returns:
    - response_data: A dictionary containing the paginated exchange rate data.
      - labels (list[str]): The x-axis dates.
      - datasets (list[dict]): A list of currency-specific datasets.
        - label (str): The currency name.
        - values (list[float]): The exchange rate values for the currency.
        - borderColor (str): The color of the dataset (optional).
      - x_label (str): The x-axis label.
      - y_label (str): The y-axis label.
    """
    logging.info("Exchange rate data requested")
    page = int(request.data.get("page", 1))
    page_size = int(request.data.get("page_size", 100))

    data = async_to_sync(load_data)("exchange")
    dates = [d for d in data.get('\ufeff"date"', [])]
    paginated_dates = dates[(page - 1) * page_size : page * page_size]

    datasets = []

    # Define colors for each currency dataset
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

            paginated_values = values[(page - 1) * page_size : page * page_size]

            # Add each currency data as a separate dataset
            datasets.append(
                {
                    "label": key.replace('"', ""),  # Remove any extra quotation marks
                    "values": paginated_values,
                    "borderColor": colors[
                        color_index % len(colors)
                    ],
                }
            )

            color_index += 1

    response_data = {
        "labels": paginated_dates,  # x-axis dates
        "datasets": datasets,  # List of currency-specific datasets
        "x_label": "Date",
        "y_label": "Exchange Rate (to CAD)",
    }

    return JsonResponse(response_data)
