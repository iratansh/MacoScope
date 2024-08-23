from django.db import models
class EconomicData(models.Model):
    indicator = models.CharField(max_length=100)
    value = models.FloatField()
    date = models.DateField()

class Prediction(models.Model):
    indicator = models.CharField(max_length=100)
    predicted_value = models.FloatField()
    date = models.DateField()
