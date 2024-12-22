import numpy as np
import logging
import pickle
import os
import aiomysql  # Async MySQL library
from keras.models import load_model  # Keras does not natively support async; will handle synchronously

# Function to load data explicitly for forecasting
async def load_data_for_forecast(indicator):
    """
    Loads data explicitly for forecasting purposes based on the indicator.
    This function queries the database and formats the data properly.
    """
    try:
        # Connect to your MySQL database asynchronously
        connection = await aiomysql.connect(
            host="macroscope-db.c928ywm8gz7k.us-east-1.rds.amazonaws.com",
            port=3306,
            user="mysqluser",
            password="secret1234",
            db="forecast_db",
        )

        async with connection.cursor(aiomysql.DictCursor) as cursor:
            if indicator == "gdp":
                query = "SELECT date, NGDPSAXDCCAQ FROM gdp"
                await cursor.execute(query)
                rows = await cursor.fetchall()
                dates = [row['date'] for row in rows]
                values = [float(row['NGDPSAXDCCAQ']) for row in rows]

            elif indicator == "unemployment":
                query = "SELECT `\ufeffProvince and Territories`, `Unemployment Rates (%)` FROM unemployment_rate"
                await cursor.execute(query)
                rows = await cursor.fetchall()
                provinces = [row['\ufeffProvince and Territories'] for row in rows]
                values = [float(row['Unemployment Rates (%)'].strip()) for row in rows]
                return provinces, values  

            elif indicator == "inflation":
                query = "SELECT date, `Inflation Rate (%)` FROM inflation"
                await cursor.execute(query)
                rows = await cursor.fetchall()
                dates = [row['date'] for row in rows]
                values = [float(row['Inflation Rate (%)']) for row in rows]

            else:
                raise ValueError(f"Invalid indicator: {indicator}. Expected one of 'gdp', 'unemployment', or 'inflation'.")

        connection.close()

        return dates, values

    except Exception as e:
        logging.error(f"Error loading data for {indicator} forecast: {e}")
        return None, None


async def make_forecast(indicator, future_periods=10):
    try:
        dates, values = await load_data_for_forecast(indicator)
        if dates is None or values is None:
            return None  

        # Convert values to a NumPy array and reshape it for LSTM input
        values = np.array(values)

        # Ensure data is properly extracted based on indicator:  Select last 5 values for forecasting
        if indicator == "gdp":
            x_input = values[-5:].reshape((1, 5, 1))  
        elif indicator == "unemployment":
            x_input = values[-5:].reshape((1, 5, 1))  
        elif indicator == "inflation":
            x_input = values[-5:].reshape((1, 5, 1))  
        else:
            raise ValueError(f"Invalid indicator: {indicator}")

        # Load the model and scaler from the file system synchronously
        model_path = os.path.join('forecasts', 'saved_models', f'{indicator.lower()}_forecasting_model.keras')
        scaler_path = os.path.join('forecasts', 'saved_models', f'{indicator.lower()}_scaler.pkl')

        model = load_model(model_path, compile=False)
        if not hasattr(model, 'optimizer') or model.optimizer is None:
            model.compile(optimizer='adam', loss='mse')

        with open(scaler_path, 'rb') as f:
            scaler = pickle.load(f)

        forecast = []
        for _ in range(future_periods):
            prediction = model.predict(x_input, verbose=0)  
            predicted_value = prediction[0][0]  
            forecast.append(predicted_value)

            # Update x_input for the next prediction
            new_step = np.array([[predicted_value]]).reshape((1, 1, 1)) 
            x_input = np.append(x_input[:, 1:, :], new_step, axis=1)  

        # Inverse transform the forecast to original scale
        forecast = np.array(forecast).reshape(-1, 1)
        forecast = scaler.inverse_transform(forecast)

        return forecast.flatten()

    except Exception as e:
        logging.error(f"Error generating forecast: {e}")
        return None
