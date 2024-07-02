from django.urls import path
from .views import (
    fetch_country_data, fetch_education_data, fetch_health_data,
    fetch_employment_data, fetch_environmental_data, fetch_economic_data,
    fetch_social_data, display_country_data, display_social_data, display_economic_data,
    display_education_data, display_employment_data, display_environment_data, display_health_data
)

urlpatterns = [
    path('fetch-country-data', fetch_country_data, name='fetch-country-data'),
    path('fetch-education-data', fetch_education_data, name='fetch-education-data'),
    path('fetch-health-data', fetch_health_data, name='fetch-health-data'),
    path('fetch-employment-data', fetch_employment_data, name='fetch-employment-data'),
    path('fetch-environmental-data', fetch_environmental_data, name='fetch-environmental-data'),
    path('fetch-economic-data', fetch_economic_data, name='fetch-economic-data'),
    path('fetch-social-data', fetch_social_data, name='fetch-social-data'),
    path('country-data', display_country_data, name='country_data'),
    path('economic-data', display_economic_data, name='economic_data'),
    path('education-data', display_education_data, name='education_data'),
    path('employment-data', display_employment_data, name='employment_data'),
    path('environmental-data', display_environment_data, name='environment_data'),
    path('health-data', display_health_data, name='health_data'),
    path('social-data', display_social_data, name='social_data'),
]
