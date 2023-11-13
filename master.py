import requests
import datetime

today = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
URL_BASE = 'http://localhost:8000/api/'


def inserisci_misurzione(id, umidita):
    url = 'igrometri/aggiungi-ultima-misurazione/'
    ultima_misurazione = {'data': today, 'umidita': umidita}
    data = {'id': id, "ultima_misurazione": ultima_misurazione}
    headers = {'Content-type': 'application/json'}

    response = requests.post(URL_BASE + url, json=data, headers=headers)

    print(response.status_code)
    print(response.json())


if __name__ == '__main__':
    inserisci_misurzione(806, 10)