from django.urls import path
from .views import (
    register, activate, logout_user, login_user, send_password_reset_email, reset_password, update_security, get_user_details, check_authentication_status
)

urlpatterns = [
    path('register/', register, name='register'),
    path('login/', login_user, name='login_user'),
    path('activate/<str:uidb64>/<str:token>/', activate, name='activate'),
    path('logout/', logout_user, name='logout_user'),
    path('forgot-password/', send_password_reset_email, name='send_password_reset_email'),
    path('update-security/', update_security, name='update_security'),
    path('account-info/', get_user_details, name='account-info'),
    path('check-auth/', check_authentication_status, name='check_authentication_status'),
    path('reset-password/<str:uidb64>/<str:token>/', reset_password, name='reset_password'),
]














