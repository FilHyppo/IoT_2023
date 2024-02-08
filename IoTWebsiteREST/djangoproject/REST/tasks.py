from celery import shared_task
from django.utils import timezone
import datetime


@shared_task
def refresh_misurazioni():
    from .models import Igrometro


    igrometri = Igrometro.objects.all()

    for igrometro in igrometri:
        misurazioni = igrometro.misurazioni
        
        # Filtra le misurazioni mantenendo solo quelle con una data successiva a una settimana fa
        misurazioni_recenti = [
            misurazione for misurazione in misurazioni
            if isinstance(misurazione, dict) and 'data' in misurazione and
               (timezone.now() - timezone.make_aware(datetime.datetime.fromisoformat(misurazione['data']))).days < 7
        ]

        deleted = len(misurazioni) - len(misurazioni_recenti)
        print(f'Eliminate {deleted} misurazioni per {igrometro.nome}')

        igrometro.misurazioni = misurazioni_recenti
        igrometro.save()

@shared_task
def trigger_irrigatori(raggio_km=10, umidita_minima=30):
    from .models import Irrigatore, Igrometro
    from mqtt_integration import tasks

    irrigatori = Irrigatore.objects.all()
    for irrigatore in irrigatori:
        igrometri_associati = irrigatore.nearest_igrometri(raggio_km)
        if len(igrometri_associati) > 0:
            media_umidita = sum([igrometro.ultima_misurazione['umidita'] for igrometro in igrometri_associati]) / len(igrometri_associati)
            if media_umidita < umidita_minima:
                tasks.sprinkle.delay(irrigatore.id, umidita_minima - media_umidita)
                print(f'Avviato irrigazione per {irrigatore.nome}')
            else:
                print(f'Irrigazione non necessaria per {irrigatore.nome}')
        else:
            print(f'Nessun igrometro associato a {irrigatore.nome}')