import os
import pickle
import tensorflow as tf
from keras.models import Sequential, load_model
from keras.layers import Dense, LSTM
from django.core.management.base import BaseCommand
from forecasts.features import create_dataset, load_data, preprocess_data, create_model
import asyncio

# Ensure Django settings are loaded
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Backend.settings')
import django
django.setup()


async def train_model(indicator):
    # Load and preprocess data asynchronously
    data = await load_data(indicator)
    data, scaler = preprocess_data(data)
    x, y = create_dataset(data)

    # Reshape for LSTM [samples, time steps, features]
    x = x.reshape((x.shape[0], x.shape[1], 1))
    
    # Create and train model
    model = create_model((x.shape[1], 1))
    model.fit(x, y, epochs=20, batch_size=32, validation_split=0.2)
    
    # Save the trained model in the new recommended format
    model.save(f'{indicator}_forecasting_model.keras')
    print(f"Model for {indicator} saved successfully.")

def create_model(input_shape):
    """
    Build and compile an LSTM model.

    Parameters:
    - input_shape: Shape of the input data (time_steps, features).

    Returns:
    - model: Compiled LSTM model.
    """
    model = Sequential()
    model.add(LSTM(50, return_sequences=True, input_shape=input_shape))
    model.add(LSTM(50))
    model.add(Dense(1))
    model.compile(optimizer='adam', loss='mse')
    return model

class Command(BaseCommand):
    help = 'Train the forecasting model for a specific economic indicator'

    def add_arguments(self, parser):
        parser.add_argument('indicator', type=str, help='Economic indicator (e.g., gdp, unemployment, inflation)')

    def handle(self, *args, **options):
        indicator = options['indicator']
        
        try:
            # Use asyncio to run the async load_data function in a synchronous context
            data = asyncio.run(load_data(indicator))
            scaled_data, scaler = preprocess_data(data)
            
            # Create dataset
            x, y = create_dataset(scaled_data, time_steps=5)
            x = x.reshape((x.shape[0], x.shape[1], 1))  # Reshape for LSTM
            
            # Build and train the model
            model = create_model((x.shape[1], 1))
            model.fit(x, y, epochs=20, batch_size=32, validation_split=0.2)
            
            # Save the model and scaler
            model_dir = os.path.join('forecasts', 'saved_models')
            os.makedirs(model_dir, exist_ok=True)
            
            model_path = os.path.join(model_dir, f'{indicator.lower()}_forecasting_model.keras')
            model.save(model_path, save_format='keras')
            
            scaler_path = os.path.join(model_dir, f'{indicator.lower()}_scaler.pkl')
            with open(scaler_path, 'wb') as f:
                pickle.dump(scaler, f)

            self.stdout.write(self.style.SUCCESS(f'Model and scaler for {indicator} saved successfully!'))

        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Error: {e}'))
