import datetime
from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIClient
from .models import Igrometro, MasterIgrometri

class IgrometroAPITest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.BASE_URL = 'http://localhost:8000/api'
        self.master_igrometri = MasterIgrometri.objects.create(nome='Master1', latitudine=40.7128, longitudine=-74.0060, quota=100.0)

    def test_crea_igrometro(self):
        data = {
            'master_id': self.master_igrometri.id, # 'master_id' è il nome del campo nel modello, 'id' è il nome del campo nel json
            'nome': 'Igrometro1',
            'latitudine': 40.7128,
            'longitudine': -74.0060,
            'attivo': True
        }
        response = self.client.post(self.BASE_URL + '/igrometri/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Igrometro.objects.count(), 1)
        self.assertEqual(Igrometro.objects.get().nome, 'Igrometro1')

    def test_aggiorna_igrometro(self):
        igrometro = Igrometro.objects.create(nome='Igrometro1', latitudine=40.7128, longitudine=-74.0060, attivo=True)
        data = {'id': igrometro.id, 'nome': 'NuovoNome', 'latitudine': 41.8781, 'longitudine': -87.6298, 'attivo': False}
        response = self.client.put(self.BASE_URL + '/igrometri/', data, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Igrometro.objects.get().nome, 'NuovoNome')
        self.assertEqual(Igrometro.objects.get().latitudine, 41.8781)
        self.assertEqual(Igrometro.objects.get().longitudine, -87.6298)
        self.assertFalse(Igrometro.objects.get().attivo)

    def test_elimina_igrometro(self):
        igrometro = Igrometro.objects.create(nome='Igrometro1', latitudine=40.7128, longitudine=-74.0060, attivo=True)
        data = {'id': igrometro.id}
        response = self.client.delete(self.BASE_URL + '/igrometri/', data, format='json')

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Igrometro.objects.count(), 0)


class MasterIgrometriAPITest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.BASE_URL = 'http://localhost:8000/api'

    def test_crea_master_igrometri(self):
        data = {
            'nome': 'Master1',
            'latitudine': 40.7128,
            'longitudine': -74.0060,
            'quota': 100.0
        }
        response = self.client.post(self.BASE_URL + '/masterigrometri/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(MasterIgrometri.objects.count(), 1)
        self.assertEqual(MasterIgrometri.objects.get().nome, 'Master1')

    def test_aggiorna_master_igrometri(self):
        master_igrometri = MasterIgrometri.objects.create(nome='Master1', latitudine=40.7128, longitudine=-74.0060, quota=100.0)
        data = {'id': master_igrometri.id, 'nome': 'NuovoMaster', 'latitudine': 41.8781, 'longitudine': -87.6298, 'quota': 200.0}
        response = self.client.put(self.BASE_URL + '/masterigrometri/', data, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(MasterIgrometri.objects.get().nome, 'NuovoMaster')
        self.assertEqual(MasterIgrometri.objects.get().latitudine, 41.8781)
        self.assertEqual(MasterIgrometri.objects.get().longitudine, -87.6298)
        self.assertEqual(MasterIgrometri.objects.get().quota, 200.0)

    def test_elimina_master_igrometri(self):
        master_igrometri = MasterIgrometri.objects.create(nome='Master1', latitudine=40.7128, longitudine=-74.0060, quota=100.0)
        data = {'id': master_igrometri.id}
        response = self.client.delete(self.BASE_URL + '/masterigrometri/', data, format='json')

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(MasterIgrometri.objects.count(), 0)

class AggiungiUltimaMisurazioneViewTest(TestCase):
    def setUp(self):
        # Crea un oggetto Igrometro per il test
        self.master = MasterIgrometri.objects.create(nome='Master1', latitudine=40.7128, longitudine=-74.0060, quota=100.0)
        self.igrometro = Igrometro.objects.create(
            master=self.master,
            nome='IgrometroTest',
            latitudine=0.0,
            longitudine=0.0,
        )
        self.BASE_URL = 'http://localhost:8000/api'

    def test_aggiungi_ultima_misurazione(self):
        url = self.BASE_URL + '/igrometri/aggiungi-ultima-misurazione/'
        data = {
            'id': self.igrometro.id,
            'ultima_misurazione': {'data': datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"), 'umidita': 50.0}
        }

        response = self.client.post(url, data, format='json', content_type='application/json')
        print(response.json())
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('message', response.json())
        self.assertEqual(response.json()['message'], 'Ultima misurazione aggiunta con successo.')

        # Verifica che i dati siano stati effettivamente salvati nel database
        igrometro = Igrometro.objects.get(id=self.igrometro.id)
        self.assertEqual(igrometro.ultima_misurazione, data['ultima_misurazione'])
        self.assertIn(data['ultima_misurazione'], igrometro.misurazioni)

