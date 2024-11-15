from django.urls import path
from .views import forecast_view, gdp_data, unemployment_data, interest_data, exchange_data, labour_data

urlpatterns = [
    path('api/predict/<str:indicator>/', forecast_view, name='forecast_view'),
    path('api/GDP/', gdp_data, name='gdp_data'),
    path('api/Unemployment/', unemployment_data, name='unemployment_data'),
    path('api/Interest Rates/', interest_data, name='interest_data'),
    path('api/Exchange Rates/', exchange_data, name='exchange_data'),
    path('api/Labour/', labour_data, name='labour_data'),
]
