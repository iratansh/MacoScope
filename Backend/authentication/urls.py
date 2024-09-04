from django.urls import path
from .views import register, activate
from .views import login_user

urlpatterns = [
    path('register/', register, name='register'),
    path('login/', login_user, name='login_user'),
    path('activate/<str:uidb64>/<str:token>/', activate, name='activate'),
]













