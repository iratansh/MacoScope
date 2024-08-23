from django.core.management.base import BaseCommand
from forecasts.train_model import train_model

class Command(BaseCommand):
    help = 'Train the machine learning model for a given economic indicator.'

    def handle(self, *args, **kwargs):
        indicator = 'GDP'  # or any other indicator you're focusing on
        train_model(indicator)
