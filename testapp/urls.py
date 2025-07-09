from django.urls import path
from .views import get_token, reset_password

urlpatterns = [
    path('api/get-token/', get_token, name='get_token'),
    path('api/reset-password/', reset_password, name='reset_password'),
]
