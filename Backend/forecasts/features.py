import numpy as np
import pandas as pd
from sklearn.preprocessing import MinMaxScaler
from django.conf import settings
import os
from forecasts.models import EconomicIndicator
from keras.models import Sequential
from keras.layers import Dense, LSTM, Dropout

def create_model(input_shape):
    """
    Build and compile an LSTM model for time series forecasting.

    Parameters:
    - input_shape: Tuple specifying the shape of the input data (time_steps, features).

    Returns:
    - model: A compiled LSTM model ready for training.
    """
    model = Sequential()
    
    # First LSTM layer with Dropout regularization
    model.add(LSTM(50, return_sequences=True, input_shape=input_shape))
    model.add(Dropout(0.2))  # Dropout layer to prevent overfitting

    # Second LSTM layer
    model.add(LSTM(50, return_sequences=True))
    model.add(Dropout(0.2))  # Dropout layer

    # Third LSTM layer (without return_sequences)
    model.add(LSTM(50))
    model.add(Dropout(0.2))  # Dropout layer

    # Output layer
    model.add(Dense(1))  # Predict a single value

    # Compile the model
    model.compile(optimizer='adam', loss='mse')
    
    return model

# forecasts/features.py
import pandas as pd
from forecasts.models import EconomicIndicator
from django.db import connection
import aiomysql

async def load_data(indicator):
    """
    Load historical economic data from the MySQL database asynchronously.

    Parameters:
    - indicator: The economic indicator to load (e.g., 'gdp', 'unemployment', 'inflation').

    Returns:
    - data: A NumPy array containing the historical values for the specified indicator.
    """
    table_mapping = {
        'gdp': 'gdp',
        'unemployment': 'unemployment_rate',  # Table name adjustment
        'inflation': 'inflation',
    }
    
    if indicator not in table_mapping:
        raise ValueError(f"Invalid indicator. Choose from: {', '.join(table_mapping.keys())}")
    
    table_name = table_mapping[indicator]
    columns = {}
    try:
        connection = await aiomysql.connect(
            host="localhost",
            port=3306,
            user="mysqluser",
            password="secret1234",
            db="forecast_db",
        )

        async with connection.cursor() as cursor:
            if indicator == 'unemployment':
                # No ordering by date, select only numeric columns
                await cursor.execute(f"SELECT `Unemployment Rates (%)` FROM {table_name}")
            else:
                # Select all columns, ordered by date for other tables
                await cursor.execute(f"SELECT * FROM {table_name} ORDER BY date")

            headers = [desc[0] for desc in cursor.description]

            # Initialize lists for each column
            for header in headers:
                columns[header] = []

            # Fetch the data row-by-row
            async for row in cursor:
                for header, value in zip(headers, row):
                    columns[header].append(value)

    finally:
        if connection:
            await connection.ensure_closed()

    df = pd.DataFrame(columns)

    if df.empty:
        raise ValueError(f"No data found for table: {table_name}")
    
    if indicator == 'unemployment':
        # Handle unemployment specifically, selecting the relevant column
        values_column = df['Unemployment Rates (%)']
    else:
        numeric_columns = df.select_dtypes(include=[np.number]).columns
        if numeric_columns.empty:
            raise ValueError(f"No numeric data found in table: {table_name}")
        values_column = df[numeric_columns[0]]
    
    return values_column.values.reshape(-1, 1)







def preprocess_data(data):
    """
    Preprocess the data by scaling it to the range [0, 1].

    Parameters:
    - data: A NumPy array of shape (n_samples, 1).

    Returns:
    - scaled_data: Scaled version of the input data.
    - scaler: The fitted MinMaxScaler object for inverse transformation.
    """
    scaler = MinMaxScaler(feature_range=(0, 1))
    scaled_data = scaler.fit_transform(data)
    return scaled_data, scaler

def create_dataset(data, time_steps=5):
    """
    Convert a time series into input-output pairs for LSTM training.

    Parameters:
    - data: The preprocessed time series data (as a NumPy array).
    - time_steps: Number of previous time steps to consider for each input sequence.

    Returns:
    - x: Input sequences as a NumPy array of shape (n_samples, time_steps, 1).
    - y: Output values as a NumPy array of shape (n_samples, 1).
    """
    x, y = [], []
    for i in range(len(data) - time_steps):
        x.append(data[i:i + time_steps, 0])
        y.append(data[i + time_steps, 0])
    return np.array(x), np.array(y)
