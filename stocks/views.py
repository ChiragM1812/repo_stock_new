import requests
from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import CountryData
from .serializers import CountryDataSerializer

# List of hardcoded countries
COUNTRIES = ['AFG', 'ALB', 'DZA', 'AND', 'AGO', 'ATG', 'ARG', 'ARM', 'AUS', 'AUT', 
    'AZE', 'BHS', 'BHR', 'BGD', 'BRB', 'BLR', 'BEL', 'BLZ', 'BEN', 'BTN', 
    'BOL', 'BIH', 'BWA', 'BRA', 'BRN', 'BGR', 'BFA', 'BDI', 'CPV', 'KHM', 
    'CMR', 'CAN', 'CAF', 'TCD', 'CHL', 'CHN', 'COL', 'COM', 'COG', 'COD', 
    'CRI', 'CIV', 'HRV', 'CUB', 'CYP', 'CZE', 'DNK', 'DJI', 'DMA', 'DOM', 
    'ECU', 'EGY', 'SLV', 'GNQ', 'ERI', 'EST', 'SWZ', 'ETH', 'FJI', 'FIN', 
    'FRA', 'GAB', 'GMB', 'GEO', 'DEU', 'GHA', 'GRC', 'GRD', 'GTM', 'GIN', 
    'GNB', 'GUY', 'HTI', 'HND', 'HUN', 'ISL', 'IND', 'IDN', 'IRN', 'IRQ', 
    'IRL', 'ISR', 'ITA', 'JAM', 'JPN', 'JOR', 'KAZ', 'KEN', 'KIR', 'PRK', 
    'KOR', 'KWT', 'KGZ', 'LAO', 'LVA', 'LBN', 'LSO', 'LBR', 'LBY', 'LIE', 
    'LTU', 'LUX', 'MDG', 'MWI', 'MYS', 'MDV', 'MLI', 'MLT', 'MHL', 'MRT', 
    'MUS', 'MEX', 'FSM', 'MDA', 'MCO', 'MNG', 'MNE', 'MAR', 'MOZ', 'MMR', 
    'NAM', 'NRU', 'NPL', 'NLD', 'NZL', 'NIC', 'NER', 'NGA', 'MKD', 'NOR', 
    'OMN', 'PAK', 'PLW', 'PAN', 'PNG', 'PRY', 'PER', 'PHL', 'POL', 'PRT', 
    'QAT', 'ROU', 'RUS', 'RWA', 'KNA', 'LCA', 'VCT', 'WSM', 'SMR', 'STP', 
    'SAU', 'SEN', 'SRB', 'SYC', 'SLE', 'SGP', 'SVK', 'SVN', 'SLB', 'SOM', 
    'ZAF', 'SSD', 'ESP', 'LKA', 'SDN', 'SUR', 'SWE', 'CHE', 'SYR', 'TWN', 
    'TJK', 'TZA', 'THA', 'TLS', 'TGO', 'TON', 'TTO', 'TUN', 'TUR', 'TKM', 
    'TUV', 'UGA', 'UKR', 'ARE', 'GBR', 'USA', 'URY', 'UZB', 'VUT', 'VEN', 
    'VNM', 'YEM', 'ZMB', 'ZWE']

WORLD_BANK_API_URL = "https://api.worldbank.org/v2/country/{country}/indicator/{indicator}?format=json&date=2020&per_page=500"

INDICATORS = {
    'gdp': 'NY.GDP.MKTP.CD',
    'inflation': 'FP.CPI.TOTL',
    'population': 'SP.POP.TOTL'
}

def fetch_indicator_data(country, indicator):
    response = requests.get(WORLD_BANK_API_URL.format(country=country, indicator=indicator))
    if response.status_code == 200:
        json_data = response.json()
        if json_data[1]:
            return json_data[1][0]['value']
    return None

def fetch_all_countries():
    countries = []
    page = 1
    while True:
        response = requests.get(f"https://api.worldbank.org/v2/country?format=json&per_page=500&page={page}")
        if response.status_code != 200:
            break
        data = response.json()
        if len(data) < 2 or not data[1]:
            break
        countries.extend(data[1])
        if len(data[1]) < 500:
            break
        page += 1
    return countries

@api_view(['GET'])
def fetch_data(request):
    CountryData.objects.all().delete()  # Delete old data

    # Fetch the list of all countries with pagination
    all_countries = fetch_all_countries()

    # Combine hardcoded countries with dynamically fetched countries
    country_codes = {country['id'] for country in all_countries}
    for country_code in COUNTRIES:
        country_codes.add(country_code)

    for country_code in country_codes:
        data = {
            'country': next((country['name'] for country in all_countries if country['id'] == country_code), country_code),
            'gdp': None,
            'inflation': None,
            'population': None
        }

        for key, indicator in INDICATORS.items():
            data[key] = fetch_indicator_data(country_code, indicator)

        CountryData.objects.create(**data)

    return Response({"status": "Data fetched and stored"})

@api_view(['GET'])
def display_data(request):
    country_data = CountryData.objects.all()
    serializer = CountryDataSerializer(country_data, many=True)
    return Response(serializer.data)
