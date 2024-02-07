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