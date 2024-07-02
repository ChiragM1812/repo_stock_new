from django.db import models

class CountryData(models.Model):
    country = models.CharField(max_length=100)
    gdp = models.FloatField(null=True, blank=True)
    inflation = models.FloatField(null=True, blank=True)
    population = models.BigIntegerField(null=True, blank=True)
    literacy_rate = models.FloatField(null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.country

class EducationData(models.Model):
    country = models.CharField(max_length=100)
    literacy_rate = models.FloatField(null=True, blank=True)
    school_enrollment_primary = models.FloatField(null=True, blank=True)
    school_enrollment_secondary = models.FloatField(null=True, blank=True)
    education_expenditure = models.FloatField(null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.country

class HealthData(models.Model):
    country = models.CharField(max_length=100)
    life_expectancy = models.FloatField(null=True, blank=True)
    mortality_rate_under_5 = models.FloatField(null=True, blank=True)
    health_expenditure = models.FloatField(null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.country

class EmploymentData(models.Model):
    country = models.CharField(max_length=100)
    unemployment_rate = models.FloatField(null=True, blank=True)
    labor_force_participation_rate = models.FloatField(null=True, blank=True)
    employment_agriculture = models.FloatField(null=True, blank=True)
    employment_industry = models.FloatField(null=True, blank=True)
    employment_services = models.FloatField(null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.country

class EnvironmentalData(models.Model):
    country = models.CharField(max_length=100)
    co2_emissions = models.FloatField(null=True, blank=True)
    access_to_clean_water = models.FloatField(null=True, blank=True) 
    renewable_energy_consumption = models.FloatField(null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.country

class EconomicData(models.Model):
    country = models.CharField(max_length=100)
    trade_balance = models.FloatField(null=True, blank=True)
    foreign_direct_investment = models.FloatField(null=True, blank=True)
    government_debt = models.FloatField(null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.country

class SocialData(models.Model):
    country = models.CharField(max_length=100)
    poverty_headcount_ratio = models.FloatField(null=True, blank=True)
    income_inequality_gini = models.FloatField(null=True, blank=True)
    social_protection_coverage = models.FloatField(null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.country
