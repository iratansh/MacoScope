import numpy as np
from .models import EconomicData

def load_data(indicator):
    data = EconomicData.objects.filter(indicator=indicator).order_by('date')
    values = np.array([d.value for d in data])
    return values

def create_dataset(data, time_step=1):
    x, y = [], []
    for i in range(len(data)-time_step-1):
        x.append(data[i:(i+time_step)])
        y.append(data[i + time_step])
    return np.array(x), np.array(y)
