import torch
from torch.utils.data import Dataset, DataLoader
import numpy as np

class IrrigationDataset(Dataset):
    def __init__(self, humidity_data, weather_data, labels):
        self.humidity_data = humidity_data
        self.weather_data = weather_data
        self.labels = labels

    def __len__(self):
        return len(self.labels)

    def __getitem__(self, idx):
        humidity_sequence = torch.tensor(self.humidity_data[idx], dtype=torch.float32)
        weather_sequence = torch.tensor(self.weather_data[idx], dtype=torch.float32)
        label = torch.tensor(self.labels[idx], dtype=torch.float32)

        return {'humidity': humidity_sequence, 'weather': weather_sequence, 'label': label}

# Esempio di creazione del dataset
humidity_data = np.random.rand(100, 10)  # 100 sequenze di umidità con 10 punti dati ciascuna
weather_data = np.random.rand(100, 10)    # 100 sequenze di dati meteorologici con 10 punti dati ciascuna
labels = np.random.randint(2, size=100)    # Etichette binarie (0 o 1)

dataset = IrrigationDataset(humidity_data, weather_data, labels)

# Creazione del data loader
batch_size = 32
data_loader = DataLoader(dataset, batch_size=batch_size, shuffle=True)
