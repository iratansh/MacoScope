import os
import pickle
import numpy as np
from keras.models import load_model

async def make_forecast(indicator, future_periods=10):
    try:
        # Load the model and scaler
        model_path = os.path.join('forecasts', 'saved_models', f'{indicator.lower()}_forecasting_model.keras')
        scaler_path = os.path.join('forecasts', 'saved_models', f'{indicator.lower()}_scaler.pkl')

        # Load the model with compile=False
        model = load_model(model_path, compile=False)

        # Ensure the model is compiled if not already done
        if not hasattr(model, 'optimizer') or model.optimizer is None:
            print("Compiling the model since optimizer is missing...")
            model.compile(optimizer='adam', loss='mse')

        # Load the scaler
        with open(scaler_path, 'rb') as f:
            scaler = pickle.load(f)

        # Example data (replace this with actual historical data)
        initial_data = np.random.rand(5, 1)  # Shape should match your model's expected input
        x_input = initial_data.reshape((1, 5, 1))  # Shape: (1, time_steps, features)

        # Generate forecast
        forecast = []
        for _ in range(future_periods):
            # Ensure the prediction has the correct shape
            prediction = model.predict(x_input, verbose=0)  # Output shape: (1, 1)
            
            # Extract the prediction value
            predicted_value = prediction[0][0]  # Shape: scalar

            # Append the forecasted value
            forecast.append(predicted_value)

            # Update x_input for the next prediction
            # Remove the oldest time step and add the new prediction
            new_step = np.array([[predicted_value]]).reshape((1, 1, 1))  # Shape: (1, 1, 1)
            x_input = np.append(x_input[:, 1:, :], new_step, axis=1)  # Shape: (1, time_steps, features)

        # Inverse transform the forecast to original scale
        forecast = np.array(forecast).reshape(-1, 1)
        forecast = scaler.inverse_transform(forecast)

        return forecast.flatten()

    except Exception as e:
        print(f"Error generating forecast: {e}")
        return None

