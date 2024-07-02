from rest_framework import serializers
from .models import CountryData, EducationData, HealthData, EmploymentData, EnvironmentalData, EconomicData, SocialData

class CountryDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = CountryData
        fields = 'country', 'gdp', 'inflation', 'population', 'literacy_rate', 'updated_at'

class EducationDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = EducationData
        fields = 'country', 'literacy_rate', 'school_enrollment_primary', 'school_enrollment_secondary', 'education_expenditure', 'updated_at'

class HealthDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = HealthData
        fields = 'country', 'life_expectancy', 'mortality_rate_under_5', 'health_expenditure', 'updated_at'

class EmploymentDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = EmploymentData
        fields = 'country', 'unemployment_rate', 'labor_force_participation_rate', 'employment_agriculture', 'employment_industry', 'employment_services', 'updated_at'

class EnvironmentalDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = EnvironmentalData
        fields = 'country', 'co2_emissions', 'access_to_clean_water', 'renewable_energy_consumption', 'updated_at'

class EconomicDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = EconomicData
        fields = 'country', 'trade_balance', 'foreign_direct_investment', 'government_debt', 'updated_at'

class SocialDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = SocialData
        fields = 'country', 'poverty_headcount_ratio', 'income_inequality_gini', 'social_protection_coverage', 'updated_at'

