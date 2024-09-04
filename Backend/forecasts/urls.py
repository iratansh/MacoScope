from django.urls import path
from .views import PredictionView, gdp_data, unemployment_data

urlpatterns = [
    path('predict/', PredictionView.as_view(), name='forecast'),
    path('api/GDP/', gdp_data, name='gdp_data'),
    path('api/Unemployment/', unemployment_data, name='unemployment_data'),
]
