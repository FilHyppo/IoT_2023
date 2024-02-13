###################### creazione dataset per RNN ########################################################
import random
import pandas as pd
import numpy as np
from datetime import datetime, timedelta

num_rows = 10000  # valori nel dataset

umidita = [random.randint(0, 100) for _ in range(num_rows)]

latitudine = [random.uniform(-90, 90) for _ in range(num_rows)]

longitudine = [random.uniform(-180, 180) for _ in range(num_rows)]

start_date = datetime.now() - timedelta(days=5 * 365)
end_date = datetime.now()
date_misurazione = [start_date + timedelta(days=random.randint(0, (end_date - start_date).days)) for _ in
                    range(num_rows)]

# Trasformazione del giorno della misurazione in valori continui
timestamp_s = pd.Series([date.timestamp() for date in date_misurazione])
day = 24 * 60 * 60
year = 365.2425 * day
day_sin = np.sin(timestamp_s * (2 * np.pi / day))
day_cos = np.cos(timestamp_s * (2 * np.pi / day))
year_sin = np.sin(timestamp_s * (2 * np.pi / year))
year_cos = np.cos(timestamp_s * (2 * np.pi / year))

# Creazione del DataFrame
df = pd.DataFrame({
    'Umidità (%)': umidita,
    'Latitudine': latitudine,
    'Longitudine': longitudine,
    'Data di misurazione': date_misurazione,
    'Day sin': day_sin,
    'Day cos': day_cos,
    'Year sin': year_sin,
    'Year cos': year_cos
})

# Stampa le prime righe del DataFrame per debug
print(df.head())

# Salva il DataFrame in un file CSV
df.to_csv('dataset_rnn.csv', index=False)

################################## creazione modello RNN################################################
import torch
import torch.nn as nn
import pandas as pd
from sklearn.model_selection import train_test_split
from torch.utils.data import Dataset, DataLoader
import numpy as np

df = pd.read_csv('dataset_rnn.csv')

# Dividi il dataset in training set e validation set
train_df, val_df = train_test_split(df, test_size=0.2, random_state=42)


# classe per il dataset
class RNNDataset(Dataset):
    def __init__(self, dataframe):
        self.data = dataframe[
            ['Umidità (%)', 'Latitudine', 'Longitudine', 'Day sin', 'Day cos', 'Year sin', 'Year cos']].values.astype(
            np.float32)
        self.targets = dataframe['Umidità (%)'].values.astype(np.float32)

    def __len__(self):
        return len(self.data)

    def __getitem__(self, idx):
        return self.data[idx], self.targets[idx]

    # rete neurale

    # rete neurale


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


# Definisci i parametri
input_size = 7  # Numero di features
hidden_size = 64
output_size = 1

# inizializza modello, la loss function e l'ottimizzatore
model = RNN(input_size, hidden_size, output_size)
criterion = nn.MSELoss()
optimizer = torch.optim.Adam(model.parameters(), lr=0.001)

# Creare i DataLoader
train_dataset = RNNDataset(train_df)
val_dataset = RNNDataset(val_df)
train_loader = DataLoader(train_dataset, batch_size=32, shuffle=True)
val_loader = DataLoader(val_dataset, batch_size=32)

# Addestramento
num_epochs = 30
for epoch in range(num_epochs):
    model.train()
    train_loss = 0.0
    for inputs, targets in train_loader:
        optimizer.zero_grad()
        # print(inputs.shape)
        outputs = model(inputs)
        # print(outputs.shape)
        loss = criterion(outputs, targets.unsqueeze(1))
        loss.backward()
        optimizer.step()
        train_loss += loss.item() * inputs.size(0)
    train_loss /= len(train_loader.dataset)

    model.eval()
    val_loss = 0.0
    with torch.no_grad():
        for inputs, targets in val_loader:
            outputs = model(inputs)
            loss = criterion(outputs, targets.unsqueeze(1))
            val_loss += loss.item() * inputs.size(0)
        val_loss /= len(val_loader.dataset)

    print(f'Epoch [{epoch + 1}/{num_epochs}], Train Loss: {train_loss:.4f}, Val Loss: {val_loss:.4f}')

# Salva il modello
torch.save(model.state_dict(), 'rnn_model.pth')

# Test del modello
sample_input = torch.tensor(
    [[50, 0.5, 0.5, 0.5, 0.5]])  # Esempio di input con umidità del 50% e segnali sinusoidali casuali
model.eval()
with torch.no_grad():
    output = model(sample_input)
    predicted_humidity = output.item()

# Calcola la quantità di irrigazione
irrigation_amount = max(0, 100 - predicted_humidity)
print(f'Umidità prevista: {predicted_humidity:.2f}%')
print(f'Quantità di irrigazione raccomandata: {irrigation_amount:.2f}%')

import matplotlib.pyplot as plt

# Carica il modello
model = RNN(input_size, hidden_size, output_size)
model.load_state_dict(torch.load('rnn_model.pth'))
model.eval()

# Esegui la predizione sul set di validazione
predictions = []
targets = []
with torch.no_grad():
    for inputs, target in val_loader:
        outputs = model(inputs)
        predictions.extend(outputs.squeeze(1).tolist())
        targets.extend(target.tolist())

# Visualizza la predizione del modello e il valore reale su un grafico
plt.figure(figsize=(10, 6))
plt.plot(targets, label='Valore reale', color='blue')
plt.plot(predictions, label='Predizione del modello', color='red')
plt.xlabel('Campione')
plt.ylabel('Umidità (%)')
plt.title('Predizione del modello vs Valore reale')
plt.legend()
plt.grid(True)
plt.show()
