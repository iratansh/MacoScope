import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', './Backend/Backend.settings')
django.setup()

from forecasts.features import create_dataset, load_data
import tensorflow as tf
from keras.models import Sequential
from keras.layers import Dense, LSTM

def create_model(input_shape):
    model = Sequential()
    model.add(LSTM(50, return_sequences=True, input_shape=input_shape))
    model.add(LSTM(50))
    model.add(Dense(1))
    model.compile(optimizer='adam', loss='mse')
    return model

def train_model(indicator):
    data = load_data(indicator)
    x, y = create_dataset(data)
    x = x.reshape((x.shape[0], x.shape[1], 1))
    model = create_model((x.shape[1], 1))
    model.fit(x, y, epochs=20, batch_size=32, validation_split=0.2)
    model.save(f'{indicator.lower()}_forecasting_model.h5')

