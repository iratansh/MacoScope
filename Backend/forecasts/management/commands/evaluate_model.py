"""
Evaluate the forecasting model for a specific economic indicator with data augmentation
"""

import os
import pickle
import numpy as np
import asyncio
from django.core.management.base import BaseCommand
from keras.models import load_model
from keras.optimizers import Adam
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score
from forecasts.features import load_data, preprocess_data, create_dataset

class Command(BaseCommand):
    help = 'Evaluate the forecasting model for a specific economic indicator with data augmentation'

    def add_arguments(self, parser):
        parser.add_argument('indicator', type=str, help='Economic indicator (e.g., gdp, unemployment, inflation)')
        parser.add_argument('--augment', type=bool, default=True, help='Enable data augmentation if dataset is small')

    def handle(self, *args, **options):
        indicator = options['indicator']
        augment = options['augment']
        
        try:
            # Load model and scaler
            model_path = os.path.join('forecasts', 'saved_models', f'{indicator.lower()}_forecasting_model.keras')
            scaler_path = os.path.join('forecasts', 'saved_models', f'{indicator.lower()}_scaler.pkl')
            model = load_model(model_path, compile=False)
            
            # Compile the model after loading
            model.compile(optimizer=Adam(), loss='mse')
            
            with open(scaler_path, 'rb') as f:
                scaler = pickle.load(f)

            # Load and preprocess data
            data = asyncio.run(load_data(indicator))
            scaled_data, _ = preprocess_data(data)

            # Augment data if the dataset is small
            if len(scaled_data) < 20 and augment:
                augmented_data = []
                for point in scaled_data:
                    noise = np.random.normal(0, 0.05, point.shape)  # add slight noise
                    noisy_point = point + noise
                    augmented_data.append(noisy_point)
                augmented_data = np.array(augmented_data)
                scaled_data = np.vstack([scaled_data, augmented_data])  # Stack to match dimensions
                self.stdout.write(self.style.SUCCESS("Data augmentation applied to unemployment dataset"))

            # Define train-test split
            train_size = int(0.8 * len(scaled_data))
            train_data, test_data = scaled_data[:train_size], scaled_data[train_size:]

            # Prepare dataset for LSTM
            x_train, y_train = create_dataset(train_data, time_steps=5)
            x_test, y_test = create_dataset(test_data, time_steps=5)

            # Ensure data has valid dimensions
            if x_train.size == 0 or x_test.size == 0:
                self.stdout.write(self.style.WARNING("Insufficient data for train-test split even after augmentation."))
                return

            x_train = x_train.reshape((x_train.shape[0], x_train.shape[1], 1))
            x_test = x_test.reshape((x_test.shape[0], x_test.shape[1], 1))

            # Train the model on the augmented dataset
            model.fit(x_train, y_train, epochs=20, batch_size=12, verbose=0)

            # Predict and evaluate
            predictions = model.predict(x_test)
            predictions = scaler.inverse_transform(predictions)
            y_test = scaler.inverse_transform(y_test.reshape(-1, 1))

            # Calculate metrics
            rmse = np.sqrt(mean_squared_error(y_test, predictions))
            mae = mean_absolute_error(y_test, predictions)
            r2 = r2_score(y_test, predictions)

            # Output results
            self.stdout.write(self.style.SUCCESS(f'Evaluation Results:'))
            self.stdout.write(self.style.SUCCESS(f'RMSE: {rmse}'))
            self.stdout.write(self.style.SUCCESS(f'MAE: {mae}'))
            self.stdout.write(self.style.SUCCESS(f'R^2: {r2}'))
        
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Error: {e}'))