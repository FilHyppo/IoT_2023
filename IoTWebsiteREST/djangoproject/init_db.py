#move to IoTWebsiteREST/djangoproject and run python3 init_db.py


import os
import django
import datetime  # Importa il modulo datetime per la gestione delle date

# Configura l'ambiente di Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'djangoproject.settings')
django.setup()

from REST.models import Igrometro, MasterIgrometri

import datetime
import random


def init_db():
    # Creare istanze di MasterIgrometri
    master1 = MasterIgrometri(nome='Master1', latitudine=45.0, longitudine=9.0, quota=100.0)
    master1.save()

    master2 = MasterIgrometri(nome='Master2', latitudine=46.0, longitudine=10.0, quota=150.0)
    master2.save()

    # Creare 30 istanze di Igrometro collegate ai MasterIgrometri con ultima misurazione


    for i in range(80):
        Igrometro(
            nome=f'Igrometro{i}', 
            latitudine=45.4643 + random.uniform(-0.04, 0.04), 
            longitudine=9.1907 + random.uniform(-0.04, 0.04), 
            master=master1, 
            ultima_misurazione={'data': datetime.datetime.now().isoformat(), 'valore': random.uniform(0.0, 100.0)}
        ).save()



def erase_db():
    # Cancella tutti i dati nei modelli
    Igrometro.objects.all().delete()
    MasterIgrometri.objects.all().delete()

if __name__ == 'main':
    erase_db()
    init_db()