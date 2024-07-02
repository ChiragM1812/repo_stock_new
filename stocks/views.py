import requests
from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import (
    CountryData, EducationData, HealthData, EmploymentData,
    EnvironmentalData, EconomicData, SocialData
)
from .serializers import (
    CountryDataSerializer, EducationDataSerializer, HealthDataSerializer,
    EmploymentDataSerializer, EnvironmentalDataSerializer, EconomicDataSerializer,
    SocialDataSerializer
)

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
    'population': 'SP.POP.TOTL',
    'literacy_rate': 'SE.ADT.LITR.ZS',
    'school_enrollment_primary': 'SE.PRM.ENRR',
    'school_enrollment_secondary': 'SE.SEC.ENRR',
    'education_expenditure': 'SE.XPD.TOTL.GD.ZS',
    'life_expectancy': 'SP.DYN.LE00.IN',
    'mortality_rate_under_5': 'SH.DYN.MORT',
    'health_expenditure': 'SH.XPD.CHEX.GD.ZS',
    'unemployment_rate': 'SL.UEM.TOTL.ZS',
    'labor_force_participation_rate': 'SL.TLF.CACT.ZS',
    'employment_agriculture': 'SL.AGR.EMPL.ZS',
    'employment_industry': 'SL.IND.EMPL.ZS',
    'employment_services': 'SL.SRV.EMPL.ZS',
    'co2_emissions': 'EN.ATM.CO2E.PC',
    'access_to_clean_water': 'SH.H2O.SAFE.ZS',
    'renewable_energy_consumption': 'EG.FEC.RNEW.ZS',
    'trade_balance': 'NE.RSB.GNFS.CD',
    'foreign_direct_investment': 'BX.KLT.DINV.CD.WD',
    'government_debt': 'GC.DOD.TOTL.GD.ZS',
    'poverty_headcount_ratio': 'SI.POV.DDAY',
    'income_inequality_gini': 'SI.POV.GINI',
    'social_protection_coverage': 'per_allsp.cov_pop_tot'
}

def fetch_indicator_data(country, indicator):
    response = requests.get(WORLD_BANK_API_URL.format(country=country, indicator=indicator))
    if response.status_code == 200:
        json_data = response.json()
        if isinstance(json_data, list) and len(json_data) > 1 and isinstance(json_data[1], list) and json_data[1]:
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

def fetch_and_store_data(model, indicators):
    model.objects.all().delete()  # Delete old data

    # Fetch the list of all countries with pagination
    all_countries = fetch_all_countries()

    # Combine hardcoded countries with dynamically fetched countries
    country_codes = {country['id'] for country in all_countries}
    for country_code in COUNTRIES:
        country_codes.add(country_code)

    for country_code in country_codes:
        data = {
            'country': next((country['name'] for country in all_countries if country['id'] == country_code), country_code)
        }

        for key, indicator in indicators.items():
            data[key] = fetch_indicator_data(country_code, indicator)

        model.objects.create(**data)

@api_view(['GET'])
def fetch_country_data(request):
    fetch_and_store_data(CountryData, {key: INDICATORS[key] for key in ['gdp', 'inflation', 'population', 'literacy_rate']})
    return Response({"status": "Country data fetched and stored"})

@api_view(['GET'])
def fetch_education_data(request):
    fetch_and_store_data(EducationData, {key: INDICATORS[key] for key in ['literacy_rate', 'school_enrollment_primary', 'school_enrollment_secondary', 'education_expenditure']})
    return Response({"status": "Education data fetched and stored"})

@api_view(['GET'])
def fetch_health_data(request):
    fetch_and_store_data(HealthData, {key: INDICATORS[key] for key in ['life_expectancy', 'mortality_rate_under_5', 'health_expenditure']})
    return Response({"status": "Health data fetched and stored"})

@api_view(['GET'])
def fetch_employment_data(request):
    fetch_and_store_data(EmploymentData, {key: INDICATORS[key] for key in ['unemployment_rate', 'labor_force_participation_rate', 'employment_agriculture', 'employment_industry', 'employment_services']})
    return Response({"status": "Employment data fetched and stored"})

@api_view(['GET'])
def fetch_environmental_data(request):
    fetch_and_store_data(EnvironmentalData, {key: INDICATORS[key] for key in ['co2_emissions', 'access_to_clean_water', 'renewable_energy_consumption']})
    return Response({"status": "Environmental data fetched and stored"})

@api_view(['GET'])
def fetch_economic_data(request):
    fetch_and_store_data(EconomicData, {key: INDICATORS[key] for key in ['trade_balance', 'foreign_direct_investment', 'government_debt']})
    return Response({"status": "Economic data fetched and stored"})

@api_view(['GET'])
def fetch_social_data(request):
    fetch_and_store_data(SocialData, {key: INDICATORS[key] for key in ['poverty_headcount_ratio', 'income_inequality_gini', 'social_protection_coverage']})
    return Response({"status": "Social data fetched and stored"})

@api_view(['GET'])
def display_country_data(request):
    country_data = CountryData.objects.all()
    serializer = CountryDataSerializer(country_data, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def display_education_data(request):
    country_data = EducationData.objects.all()
    serializer = EducationDataSerializer(country_data, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def display_health_data(request):
    country_data = HealthData.objects.all()
    serializer = HealthDataSerializer(country_data, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def display_employment_data(request):
    country_data = EmploymentData.objects.all()
    serializer = EmploymentDataSerializer(country_data, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def display_environment_data(request):
    country_data = EnvironmentalData.objects.all()
    serializer = EnvironmentalDataSerializer(country_data, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def display_economic_data(request):
    country_data = EconomicData.objects.all()
    serializer = EconomicDataSerializer(country_data, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def display_social_data(request):
    social_data = SocialData.objects.all()
    serializer = SocialDataSerializer(social_data, many=True)
    return Response(serializer.data)