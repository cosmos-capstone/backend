
from django.db import models
from keras._tf_keras.keras.models import load_model
import numpy as np
from datetime import datetime, timedelta
import FinanceDataReader as fdr
from sklearn.preprocessing import StandardScaler
import os
from pathlib import Path

class Prediction(models.Model):
    symbol = models.CharField(max_length=10)
    BASE_DIR = Path(__file__).resolve().parent

    @staticmethod
    def get_stock_pred(symbol):
        if '.' in symbol:
            symbol = symbol.split('.')[0]
        model_path = os.path.join(Prediction.BASE_DIR, 'save_models', f'lstm_{symbol}.keras')
            
        try:
            model = load_model(model_path)
        except:
            print("No model found")
            
        end_date = datetime.now().strftime('%Y-%m-%d')
        start_date = (datetime.now() - timedelta(days=20)).strftime('%Y-%m-%d')
        data = fdr.DataReader(symbol, start_date, end_date)
        
        scaler = StandardScaler()
        data_scaled = scaler.fit_transform(data[['Open', 'High', 'Low', 'Close', 'Volume']])
        last_sequence = data_scaled[-10:]
        days_ahead = 10
        
        prediction = Prediction.multi_step_forecast(model, last_sequence, days_ahead, scaler)
        prediction_dates = [(datetime.now() + timedelta(days=i)).strftime('%Y-%m-%d') for i in range(1, days_ahead + 1)]
        return prediction_dates, prediction
    @staticmethod
    def multi_step_forecast(model, last_sequence, days_ahead, scaler):
            forecast = []
            sequence = last_sequence.copy()
            
            for _ in range(days_ahead):
                prediction = model.predict(sequence[np.newaxis, :, :])
                prediction = np.repeat(prediction, sequence.shape[1], axis=-1)
                
                sequence = np.append(sequence[1:], prediction, axis=0)
                
                mean_values_pred = np.repeat(scaler.mean_[np.newaxis, :], 1, axis=0)
                mean_values_pred[:, 0] = prediction[0, 0]
                y_pred_original = scaler.inverse_transform(mean_values_pred)[:, 0]
                
                forecast.append(y_pred_original[0])

            return forecast
        
