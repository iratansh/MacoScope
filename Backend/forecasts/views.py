from rest_framework.views import APIView
from keras.models import load_model
from .features import load_data
from django.http import JsonResponse
from rest_framework.response import Response
from rest_framework.decorators import api_view
import logging

class PredictionView(APIView):
    def get(self, request, indicator):
        data = load_data(indicator)
        model = load_model(f'{indicator.lower()}_forecasting_model.h5')
        data = data[-10:].reshape((1, 10, 1))  
        prediction = model.predict(data)
        return JsonResponse({'prediction': prediction[0][0]})


@api_view(['POST'])
def gdp_data(request):
    logging.info('GDP data requested')
    # test restapi with some made up data
    data = {
        "labels": ["2018", "2019", "2020", "2021", "2022"],
        "values": [1.8, 1.9, -2.1, 5.0, 3.2],
        "label": "GDP Growth Rate (%)"
    }
    return JsonResponse(data)

@api_view(['POST'])
def unemployment_data(request):
    # test restapi with some made up data
    data = {
        "labels": ["2018", "2019", "2020", "2021", "2022"],
        "values": [5.8, 5.7, 9.5, 7.5, 6.9],
        "label": "Unemployment Rate (%)"
    }
    return JsonResponse(data)

