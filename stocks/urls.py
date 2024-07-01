from django.urls import path
from .views import fetch_data, display_data

urlpatterns = [
    path('fetch', fetch_data, name='fetch_data'),
    path('crypto', display_data, name='display_data'),
]
