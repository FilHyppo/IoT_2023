import math
import numpy as np
import pandas as pd
import torch
from torch import nn

class RNN(nn.Module):
    def __init__(self, input_size, hidden_size, output_size):
        super(RNN, self).__init__()
        self.hidden_size = hidden_size
        self.lstm = nn.LSTM(input_size, hidden_size, batch_first=True)
        self.fc = nn.Linear(hidden_size, output_size)

    def forward(self, x):
        x = x.unsqueeze(1)
        lstm_out, _ = self.lstm(x)
        out = self.fc(lstm_out[:, -1, :])
        return out


def predict(lista_umidita, lat, lon, day_sin, day_cos, year_sin, year_cos):
    input_size = 17  # Numero di features
    hidden_size = 128
    output_size = 1
    model = RNN(input_size, hidden_size, output_size)
    params = torch.load('AI/rnn_model.pth')
    model.load_state_dict(params)
    model.eval()
    with torch.no_grad():
        input = [u for u in lista_umidita] + [1, lat, lon, day_sin, day_cos, year_sin, year_cos]
        #rendilo un tensore
        input_tensor = torch.tensor([input], dtype=torch.float32)
        #print(f'input_tensor: {input_tensor}')
        output = model(input_tensor)
        irrigation_amount = int(output.item())
        print(f'irrigation_amount: {irrigation_amount}')
        return irrigation_amount


def sinusoidal_date(date):
    # Calcola il giorno dell'anno (da 1 a 365 o 366)
    day_of_year = date.timetuple().tm_yday
    
    # Calcola gli angoli per il giorno dell'anno
    day_angle = (2 * math.pi * day_of_year) / 365
    
    # Calcola i valori sinusoidali e cosinusoidali per il giorno dell'anno
    day_sin = math.sin(day_angle)
    day_cos = math.cos(day_angle)
    
    # Calcola gli angoli per l'anno
    year_angle = (2 * math.pi * date.year) / 365
    
    # Calcola i valori sinusoidali e cosinusoidali per l'anno
    year_sin = math.sin(year_angle)
    year_cos = math.cos(year_angle)
    
    return day_sin, day_cos, year_sin, year_cos

def predict_duration(lista_umidita,lat, lon, date):
    if len(lista_umidita) < 10:
        #aggiungi in coda l'ultimo valore di umidità finché non raggiungi 10
        for _ in range(10-len(lista_umidita)):
            lista_umidita.append(lista_umidita[-1])
    day_sin, day_cos, year_sin, year_cos = sinusoidal_date(date)
    return predict(lista_umidita, lat, lon, day_sin, day_cos, year_sin, year_cos)
    