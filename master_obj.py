import requests
import datetime
import argparse

class Master:
    def __init__(self, base_url='http://localhost:8000/api/'):
        self.base_url = base_url

    def _make_request(self, method, url, data=None):
        headers = {'Content-type': 'application/json'}
        response = requests.request(method, self.base_url + url, json=data, headers=headers)
        return response

    def get_current_date(self):
        return datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    def inserisci_misurazione(self, id, umidita):
        url = 'igrometri/aggiungi-ultima-misurazione/'
        ultima_misurazione = {'data': self.get_current_date(), 'umidita': umidita}
        data = {'id': id, "ultima_misurazione": ultima_misurazione}
        response = self._make_request('POST', url, data)
        print(response.status_code)
        print(response.json())

    def crea_igrometro(self, master_id, nome, latitudine, longitudine, attivo):
        url = 'igrometri/'
        data = {'master_id': master_id, 'nome': nome, 'latitudine': latitudine, 'longitudine': longitudine, 'attivo': attivo}
        response = self._make_request('POST', url, data)
        print(response.status_code)
        print(response.json())

    def elimina_igrometro(self, id):
        url = 'igrometri/'
        data = {'id': id}
        response = self._make_request('DELETE', url, data)
        print(response.status_code)
        try:
            print(response.json())
        except:
            pass

    def aggiorna_igrometro(self, id, master_id=None, nome=None, latitudine=None, longitudine=None, attivo=None):
        url = 'igrometri/'
        data = {'id': id}
        if master_id is not None:
            data['master_id'] = master_id
        if nome is not None:
            data['nome'] = nome
        if latitudine is not None:
            data['latitudine'] = latitudine
        if longitudine is not None:
            data['longitudine'] = longitudine
        if attivo is not None:
            data['attivo'] = attivo
        response = self._make_request('PUT', url, data)
        print(response.status_code)
        print(response.json())

    def crea_master(self, nome, latitudine, longitudine, quota):
        url = 'masterigrometri/'
        data = {'nome': nome, 'latitudine': latitudine, 'longitudine': longitudine, 'quota': quota}
        response = self._make_request('POST', url, data)
        print(response.status_code)
        print(response.json())

    def elimina_master(self, id):
        url = 'masterigrometri/'
        data = {'id': id}
        response = self._make_request('DELETE', url, data)
        print(response.status_code)
        try:
            print(response.json())
        except:
            pass

    def aggiorna_master(self, id, nome=None, latitudine=None, longitudine=None, quota=None):
        url = 'masterigrometri/'
        data = {'id': id}
        if nome is not None:
            data['nome'] = nome
        if latitudine is not None:
            data['latitudine'] = latitudine
        if longitudine is not None:
            data['longitudine'] = longitudine
        if quota is not None:
            data['quota'] = quota
        response = self._make_request('PUT', url, data)
        print(response.status_code)
        print(response.json())


if __name__ == '__main__':
    parser = argparse.ArgumentParser()

    parser.add_argument('--model', choices=['igrometro', 'master'], required=True, help='Select model')
    parser.add_argument('--method', choices=['create', 'update', 'delete', 'insert'], required=True, help='Select method')

    parser.add_argument('--masterID', type=int, required=False, help='Select master id')
    parser.add_argument('--name', type=str, required=False, help='Select name')
    parser.add_argument('--lat', type=float, required=False, help='Select latitude')
    parser.add_argument('--lon', type=float, required=False, help='Select longitude')
    parser.add_argument('--alt', type=float, required=False, help='Select altitude')

    parser.add_argument('--id', type=int, required=False, help='Select id')
    parser.add_argument('--humidity', type=float, required=False, help='Select humidity')

    args = parser.parse_args()

    master = Master()

    if args.method == 'create':
        if args.model == 'igrometro':
            if args.masterID is None or args.name is None or args.lat is None or args.lon is None:
                print('Errore: è necessario specificare --masterID, --name, --lat e --lon')
            else:
                master.crea_igrometro(args.masterID, args.name, args.lat, args.lon, True)

        elif args.model == 'master':
            if args.name is None or args.lat is None or args.lon is None or args.alt is None:
                print('Errore: è necessario specificare --name, --lat, --lon e --alt')
            else:
                master.crea_master(args.name, args.lat, args.lon, args.alt)

        else:
            print('Model not found')

    elif args.method == 'insert':
        if args.model == 'igrometro':
            if args.id is None or args.humidity is None:
                print('Errore: è necessario specificare --id e --humidity')
            else:
                master.inserisci_misurazione(args.id, args.humidity)
        else:
            print('Model not found')

    elif args.method == 'update':
        if args.model == 'igrometro':
            if args.id is None or (args.masterID is None and args.name is None and args.lat is None and args.lon is None and args.alt is None):
                print('Errore: è necessario specificare --id e almeno uno tra --masterID, --name, --lat, --lon e --alt')
            else:
                master.aggiorna_igrometro(args.id, args.masterID, args.name, args.lat, args.lon, args.alt)
        elif args.model == 'master':
            if args.id is None or (args.name is None and args.lat is None and args.lon is None and args.alt is None):
                print('Errore: è necessario specificare --id e almeno uno tra --name, --lat, --lon e --alt')
            else:
                master.aggiorna_master(args.id, args.name, args.lat, args.lon, args.alt)
        else:
            print('Model not found')

    elif args.method == 'delete':
        if args.model == 'igrometro':
            if args.id is None:
                print('Errore: è necessario specificare --id')
            else:
                master.elimina_igrometro(args.id)
        elif args.model == 'master':
            if args.id is None:
                print('Errore: è necessario specificare --id')
            else:
                master.elimina_master(args.id)
        else:
            print('Model not found')

    else:
        print('Method not found')
