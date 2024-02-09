from celery import shared_task
from django.utils import timezone
from django.conf import settings
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
def trigger_logic(id_irrigatore):
    from .models import Irrigatore
    from mqtt_integration import tasks
    irrigatore = Irrigatore.objects.get(id=id_irrigatore)
    igrometri_associati = irrigatore.nearest_igrometri(raggio_km=10)
    print(f'Trovati {len(igrometri_associati)} igrometri associati a {irrigatore.nome}')
    if len(igrometri_associati) > 0:
        prediction = ...
        media_umidita = sum([igrometro.ultima_misurazione['umidita'] if igrometro.ultima_misurazione else 0
                              for igrometro in igrometri_associati]) / len(igrometri_associati)
        print(f'Media umidità: {media_umidita} per {irrigatore.nome}')
        if media_umidita < settings.UMIDITA_MINIMA_IRRIGAZIONE:
            tasks.sprinkle.delay(irrigatore.secret, settings.UMIDITA_MINIMA_IRRIGAZIONE - media_umidita)
            print(f'Avviato irrigazione per {irrigatore.nome}')
        else:
            print(f'Irrigazione non necessaria per {irrigatore.nome}')
    else:
        print(f'Nessun igrometro associato a {irrigatore.nome}')


@shared_task
def trigger_irrigatori(raggio_km=10):
    from .models import Irrigatore, Igrometro
    from mqtt_integration import tasks

    irrigatori = Irrigatore.objects.all()
    for irrigatore in irrigatori:
        trigger_logic.delay(irrigatore.id)