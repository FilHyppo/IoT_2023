import datetime
from django.test import RequestFactory, TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient, APIRequestFactory
from .models import Igrometro, MasterIgrometri


SERVER_NAME = 'localhost'
PORT = 8000


class IgrometroAPITest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.url = f'http://{SERVER_NAME}:{PORT}/api/igrometri/'
        self.master_igrometri = MasterIgrometri.objects.create(nome='Master1', latitudine=40.7128, longitudine=-74.0060, quota=100.0)

    def test_crea_igrometro(self):
        data = {
            'master_id': self.master_igrometri.id, # 'master_id' è il nome del campo nel modello, 'id' è il nome del campo nel json
            'nome': 'Igrometro1',
            'latitudine': 40.7128,
            'longitudine': -74.0060,
            'attivo': True
        }
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Igrometro.objects.count(), 1)
        self.assertEqual(Igrometro.objects.get().nome, 'Igrometro1')

    def test_aggiorna_igrometro(self):
        igrometro = Igrometro.objects.create(nome='Igrometro1', latitudine=40.7128, longitudine=-74.0060, attivo=True)
        data = {'nome': 'NuovoNome', 'latitudine': 41.8781, 'longitudine': -87.6298, 'attivo': False}
        response = self.client.put(self.url + f'{igrometro.id}/', data, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Igrometro.objects.get().nome, 'NuovoNome')
        self.assertEqual(Igrometro.objects.get().latitudine, 41.8781)
        self.assertEqual(Igrometro.objects.get().longitudine, -87.6298)
        self.assertFalse(Igrometro.objects.get().attivo)

    def test_elimina_igrometro(self):
        igrometro = Igrometro.objects.create(nome='Igrometro1', latitudine=40.7128, longitudine=-74.0060, attivo=True)
        response = self.client.delete(self.url + f'{igrometro.id}/')

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Igrometro.objects.count(), 0)

    def test_crea_igrometro_errore_master_non_esiste(self):
        data = {
            'master_id': 999,  # ID inesistente
            'nome': 'Igrometro1',
            'latitudine': 40.7128,
            'longitudine': -74.0060,
            'attivo': True
        }
        response = self.client.post(self.url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_aggiorna_igrometro_errore_igrometro_non_esiste(self):
        data = {'nome': 'NuovoNome', 'latitudine': 41.8781, 'longitudine': -87.6298, 'attivo': False}
        response = self.client.put(self.url + '999/', data, format='json')

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(response.json(), {'error': 'L\'igrometro specificato non esiste.'})

    def test_elimina_igrometro_errore_igrometro_non_esiste(self):
        response = self.client.delete(self.url + '999/')

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(response.json(), {'error': 'L\'igrometro specificato non esiste.'})

class MasterIgrometriAPITest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.url = F'http://{SERVER_NAME}:{PORT}/api/masterigrometri/'

    def test_crea_master_igrometri(self):
        data = {
            'nome': 'Master1',
            'latitudine': 40.7128,
            'longitudine': -74.0060,
            'quota': 100.0
        }
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(MasterIgrometri.objects.count(), 1)
        self.assertEqual(MasterIgrometri.objects.get().nome, 'Master1')

    def test_aggiorna_master_igrometri(self):
        master_igrometri = MasterIgrometri.objects.create(nome='Master1', latitudine=40.7128, longitudine=-74.0060, quota=100.0)
        data = {'nome': 'NuovoMaster', 'latitudine': 41.8781, 'longitudine': -87.6298, 'quota': 200.0}
        response = self.client.put(self.url + f'{master_igrometri.id}/', data, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(MasterIgrometri.objects.get().nome, 'NuovoMaster')
        self.assertEqual(MasterIgrometri.objects.get().latitudine, 41.8781)
        self.assertEqual(MasterIgrometri.objects.get().longitudine, -87.6298)
        self.assertEqual(MasterIgrometri.objects.get().quota, 200.0)

    def test_elimina_master_igrometri(self):
        master_igrometri = MasterIgrometri.objects.create(nome='Master1', latitudine=40.7128, longitudine=-74.0060, quota=100.0)
        response = self.client.delete(self.url + f'{master_igrometri.id}/')

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(MasterIgrometri.objects.count(), 0)

    def test_elimina_master_igrometri_errore_master_non_esiste(self):
        response = self.client.delete(self.url + f'999/')

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(response.json(), {'error': 'Il master specificato non esiste.'})

    def test_aggiorna_master_igrometri_errore_master_non_esiste(self):
        data = {'name': 'ciao'}
        response = self.client.put(self.url + '999/', data, format='json')

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(response.json(), {'error': 'Il master specificato non esiste.'})

class MisurazioneViewTest(TestCase):
    def setUp(self):
        # Crea un oggetto Igrometro per il test
        self.master = MasterIgrometri.objects.create(nome='Master1', latitudine=40.7128, longitudine=-74.0060, quota=100.0)
        self.igrometro = Igrometro.objects.create(
            master=self.master,
            nome='IgrometroTest',
            latitudine=0.0,
            longitudine=0.0,
        )

    def get_url(self, id):
        return f'http://{SERVER_NAME}:{PORT}/api/igrometri/{id}/misurazioni/'

    def test_aggiungi_e_cancella_ultima_misurazione(self):
        data = {
            'ultima_misurazione': {'data': datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"), 'umidita': 50.0}
        }

        response = self.client.post(self.get_url(self.igrometro.id), data, format='json', content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('message', response.json())
        self.assertEqual(response.json()['message'], 'Ultima misurazione aggiunta con successo.')

        # Verifica che i dati siano stati effettivamente salvati nel database
        igrometro = Igrometro.objects.get(id=self.igrometro.id)
        self.assertEqual(igrometro.ultima_misurazione, data['ultima_misurazione'])
        self.assertIn(data['ultima_misurazione'], igrometro.misurazioni)


        response = self.client.delete(self.get_url(self.igrometro.id))
        # Verifica che la risposta sia corretta
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json(), {'message': 'Ultima misurazione cancellata con successo.'})

        # Verifica che l'ultima misurazione sia stata effettivamente rimossa
        self.assertEqual(Igrometro.objects.get(id=self.igrometro.id).misurazioni, [])
        self.assertIsNone(Igrometro.objects.get(id=self.igrometro.id).ultima_misurazione)
        
    def test_cancella_ultima_misurazione_errore_igrometro_non_esiste(self):
        # Costruisci l'URL per la vista
        # Esegui una richiesta DELETE con un ID inesistente all'URL
        response = self.client.delete(self.get_url(999))
        # Verifica che la risposta sia corretta
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        print(response.content)
        self.assertEqual(response.json(), {'error': 'L\'igrometro specificato non esiste.'})

    def test_cancella_ultima_misurazione_errore_nessuna_misurazione_da_cancellare(self):
        # Rimuovi l'ultima misurazione in modo che non ce ne siano
        self.igrometro.misurazioni = None
        self.igrometro.misurazioni = None
        # Costruisci l'URL per la vista
        response = self.client.delete(self.get_url(self.igrometro.id))
        # Verifica che la risposta sia corretta
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.json(), {'error': 'Nessuna misurazione da cancellare.'})
