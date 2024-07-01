from django.db import models

class CountryData(models.Model):
    country = models.CharField(max_length=100)
    gdp = models.FloatField(null=True, blank=True)
    inflation = models.FloatField(null=True, blank=True)
    population = models.BigIntegerField(null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.country
