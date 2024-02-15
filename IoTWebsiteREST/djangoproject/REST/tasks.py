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

def get_lista_umidita(igrometri_associati):
    lista_umidita = []
    for igrometro in igrometri_associati:
        misurazioni = igrometro.misurazioni
        #ogni misurazione è un dizionario con chiave 'data' e 'umidita'
        #filtra le misrazioni più recenti di un giorni
        misurazioni_recenti = [
            misurazione for misurazione in misurazioni
            if isinstance(misurazione, dict) and 'data' in misurazione and
               (timezone.now() - timezone.make_aware(datetime.datetime.fromisoformat(misurazione['data']))).days < 1
        ]
        #estrae solo i valori di umidità
        umidita = [misurazione['umidita'] for misurazione in misurazioni_recenti]
        #aggiunge la media delle misurazioni recenti alla lista
        lista_umidita.append(sum(umidita)/len(umidita))
    return lista_umidita


@shared_task
def trigger_logic(id_irrigatore):
    from .models import Irrigatore
    from mqtt_integration import tasks
    from AI import tasks as ai_tasks

    irrigatore = Irrigatore.objects.get(id=id_irrigatore)
    igrometri_associati = irrigatore.nearest_igrometri(raggio_km=10)
    if len(igrometri_associati) > 0:
        lista_umidita = get_lista_umidita(igrometri_associati)
        prediction = ai_tasks.predict_duration(
            lista_umidita=lista_umidita,
            lat=irrigatore.latitudine,
            lon=irrigatore.longitudine,
            date=timezone.now()
        )
        
        tasks.sprinkle.delay(irrigatore.id, prediction)
        #print(f'Avviato irrigazione per {irrigatore.nome}')
    else:
        print(f'WARNING: Nessun igrometro associato a {irrigatore.nome}')


@shared_task
def trigger_irrigatori(raggio_km=10):
    from .models import Irrigatore, Igrometro
    from mqtt_integration import tasks

    irrigatori = Irrigatore.objects.all()
    for irrigatore in irrigatori:
        trigger_logic.delay(irrigatore.id)