import os
import urllib.request
import zipfile

import numpy as np
import pandas as pd
import torch
from torch.utils.data import Dataset
from tqdm.notebook import tqdm


class WeatherJenaDataset(Dataset):
    MEAN = [9.88656343e+02, 9.10820659e+00, 2.83194958e+02, 4.59960541e+00,
            7.59060084e+01, 1.33550981e+01, 9.35695962e+00, 3.99805597e+00,
            5.91355033e+00, 9.46637099e+00, 1.21699436e+03, -5.94181630e-01,
            -3.91512714e-01, -9.62158759e-01, -7.09400721e-01, -5.43022767e-05,
            -7.24215306e-05, 5.28237873e-02, -1.62425716e-02]
    STD = [8.29746565, 8.65494994, 8.72474584, 6.97227477, 16.55533649,
           7.69473767, 4.20825963, 4.8177406, 2.67125215, 4.26005455,
           40.95770444, 2.0129306, 1.56150746, 3.12732207, 2.61966312,
           0.70709063, 0.70713733, 0.70062267, 0.71140285]

    def download_dataset(self, root, download):
        path = os.path.join(*[root, 'data.pkl'])
        if not os.path.exists(path) and download:
            # download dataset and import with pandas
            url = 'https://storage.googleapis.com/tensorflow/tf-keras-datasets/jena_climate_2009_2016.csv.zip'
            print('Downloading dataset...')
            filehandle, _ = urllib.request.urlretrieve(url)
            zip_file_object = zipfile.ZipFile(filehandle, 'r')
            first_file = zip_file_object.namelist()[0]
            df = pd.read_csv(zip_file_object.open(first_file, 'r'))
            df = self.prepare_dataset(df)
            os.makedirs(root, exist_ok=True)
            pd.to_pickle(df, path)
            print('Download complete!')
        else:
            assert os.path.exists(path)
            df = pd.read_pickle(path)
            print('Files already downloaded and verified')
        return df

    def prepare_dataset(self, df):
        # subsample
        print(df.shape, self.__dir__())
        df = df.iloc[5::self.subsample_rate]
        date_time = pd.to_datetime(df.pop('Date Time'), format='%d.%m.%Y %H:%M:%S')

        # decompose wind speed
        wv = df['wv (m/s)']
        bad_wv = wv == -9999.0
        wv[bad_wv] = 0.0
        max_wv = df['max. wv (m/s)']
        bad_max_wv = max_wv == -9999.0
        max_wv[bad_max_wv] = 0.0
        # df['wv (m/s)'].min()
        wv = df.pop('wv (m/s)')
        max_wv = df.pop('max. wv (m/s)')
        wd_rad = df.pop('wd (deg)') * np.pi / 180
        df['Wx'] = wv * np.cos(wd_rad)
        df['Wy'] = wv * np.sin(wd_rad)
        df['max Wx'] = max_wv * np.cos(wd_rad)
        df['max Wy'] = max_wv * np.sin(wd_rad)

        # decompose day/year signal
        day = 24 * 60 * 60
        year = (365.2425) * day
        timestamp_s = date_time.map(pd.Timestamp.timestamp)
        df['Day sin'] = np.sin(timestamp_s * (2 * np.pi / day))
        df['Day cos'] = np.cos(timestamp_s * (2 * np.pi / day))
        df['Year sin'] = np.sin(timestamp_s * (2 * np.pi / year))
        df['Year cos'] = np.cos(timestamp_s * (2 * np.pi / year))

        return df

    def split_dataset(self, df, train):
        n = len(df)
        if train:
            return df[0:int(n * 0.7)]
        else:
            return df[int(n * 0.7):]

    def __init__(self, root, input_width=12, label_shift=2, train=True, download=True, subsample_rate=6):
        super().__init__()
        self.subsample_rate = subsample_rate
        self.label_shift = label_shift
        self.input_width = input_width
        self.ds = self.split_dataset(self.download_dataset(root, download), train)

    def __len__(self):
        return len(self.ds) - self.input_width - self.label_shift

    def __getitem__(self, idx):
        x = self.ds.iloc[idx:idx + self.input_width].values
        y = self.ds.iloc[idx + self.input_width + self.label_shift]['T (degC)'].astype('float32')
        x = torch.tensor((x - np.array(self.MEAN)) / np.array(self.STD)).float()
        return x, y
    
import matplotlib.pyplot as plt

x, y = next(iter(train_dl))
print(x.shape)
print(x[0])
plt.figure(figsize=(20, 3))
for i in range(len(x[::12])):
    plt.plot(np.arange(len(x[i])) + i * 14, x[i][:, 1] * train_ds.STD[1] + train_ds.MEAN[1], c='blue', marker='o')
    plt.scatter([13 + i * 14], [y[i]], color='red', marker='x')

plt.ylabel('Temp')
plt.xlabel('Timestep')
plt.show()