import torch
import torch.nn as nn
from torch.utils.data import DataLoader
from .dataset import IrrigationDataset


class LSTMModel(nn.Module):
    def __init__(self, input_size, hidden_size, output_size):
        super(LSTMModel, self).__init__()
        self.lstm = nn.LSTM(input_size, hidden_size, batch_first=True)
        self.fc = nn.Linear(hidden_size, output_size)

    def forward(self, x):
        out, _ = self.lstm(x)
        out = self.fc(out[:, -1, :])  # Usa solo l'output all'ultimo passo temporale
        return out


def evaluate_model(model, data_loader, criterion):
    model.eval()
    with torch.no_grad():
        total_loss = 0.0
        for batch in data_loader:
            inputs = batch['concatenated_data']
            labels = batch['label']

            outputs = model(inputs)
            loss = criterion(outputs, labels)
            total_loss += loss.item() * inputs.size(0)

        average_loss = total_loss / len(data_loader.dataset)
        return average_loss

input_size = ... # Dimensione dell'input (ad esempio, numero di feature dell'umidità e del meteo)
hidden_size = ...  # Dimensione dello stato nascosto LSTM
output_size = 1  # Output binario (0 o 1 per decidere se innaffiare o meno)

model = LSTMModel(input_size, hidden_size, output_size)

learning_rate = 0.001
num_epochs = 10
data_loader = ... #TODO: inserire il dataloader


criterion = nn.BCEWithLogitsLoss()
optimizer = torch.optim.Adam(model.parameters(), lr=learning_rate)

for epoch in range(num_epochs):
    for batch in data_loader:
        inputs = batch['concatenated_data']  # Concatena dati di umidità e meteo
        labels = batch['label']

        optimizer.zero_grad()
        outputs = model(inputs)
        loss = criterion(outputs, labels)
        loss.backward()
        optimizer.step()


