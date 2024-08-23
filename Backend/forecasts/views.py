from rest_framework.views import APIView
from rest_framework.response import Response
from keras.models import load_model
from .features import load_data

class PredictionView(APIView):
    def get(self, request, indicator):
        data = load_data(indicator)
        model = load_model(f'{indicator.lower()}_forecasting_model.h5')
        data = data[-10:].reshape((1, 10, 1))  
        prediction = model.predict(data)
        return Response({'prediction': prediction[0][0]})

