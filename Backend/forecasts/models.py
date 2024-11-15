from django.db import models

class EconomicIndicator(models.Model):
    date = models.DateField()
    gdp = models.FloatField(null=True, blank=True)
    unemployment_rate = models.FloatField(null=True, blank=True)
    interest_rate = models.FloatField(null=True, blank=True)
    labour_rate = models.FloatField(null=True, blank=True)
    exchange_rate = models.FloatField(null=True, blank=True)

    def __str__(self):
        return f"Data for {self.date}"
    
    class Meta:
        db_table = 'economic_indicator'
        app_label = 'forecasts'  



class Prediction(models.Model):
    indicator = models.CharField(max_length=100)
    predicted_value = models.FloatField()
    date = models.DateField()
