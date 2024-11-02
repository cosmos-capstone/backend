from django.test import TestCase
from django.db import models
from datetime import datetime, timedelta
import numpy as np
from pathlib import Path
import os

from keras._tf_keras.keras.models import load_model
import FinanceDataReader as fdr
from sklearn.preprocessing import StandardScaler
import keras
os.environ['TF_ENABLE_ONEDNN_OPTS'] = '0'

print(fdr.__version__)
print(keras.__version__)

# BASE_DIR = Path(__file__).resolve().parent


# def get_stock_pred(symbol):
#     if '.' in symbol:
#         symbol = symbol.split('.')[0]
#     model_path = os.path.join(BASE_DIR, 'save_models', f'lstm_{symbol}.keras')
        
#     try:
#         model = load_model(model_path)
#     except:
#         print("No model found")
        
#     end_date = datetime.now().strftime('%Y-%m-%d')
#     start_date = (datetime.now() - timedelta(days=20)).strftime('%Y-%m-%d')
#     data = fdr.DataReader(symbol, start_date, end_date)
    
#     scaler = StandardScaler()
#     data_scaled = scaler.fit_transform(data[['Open', 'High', 'Low', 'Close', 'Volume']])
#     last_sequence = data_scaled[-10:]
#     days_ahead = 7
    
#     prediction = multi_step_forecast(model, last_sequence, days_ahead, scaler)
#     prediction_dates = [(datetime.now() + timedelta(days=i)).strftime('%Y-%m-%d') for i in range(1, days_ahead + 1)]
#     return prediction_dates, prediction
# def multi_step_forecast(model, last_sequence, days_ahead, scaler):
#         forecast = []
#         sequence = last_sequence.copy()
        
#         for _ in range(days_ahead):
#             prediction = model.predict(sequence[np.newaxis, :, :])
#             prediction = np.repeat(prediction, sequence.shape[1], axis=-1)
            
#             sequence = np.append(sequence[1:], prediction, axis=0)
            
#             mean_values_pred = np.repeat(scaler.mean_[np.newaxis, :], 1, axis=0)
#             mean_values_pred[:, 0] = prediction[0, 0]
#             y_pred_original = scaler.inverse_transform(mean_values_pred)[:, 0]
            
#             forecast.append(y_pred_original[0])

#         return forecast

# print(get_stock_pred('SPY'))