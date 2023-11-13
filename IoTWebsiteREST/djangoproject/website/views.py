from django.contrib.auth import logout
from django.contrib.auth.views import LoginView
from django.shortcuts import render
from django.contrib.auth.decorators import user_passes_test
from REST.models import Igrometro, MasterIgrometri
from django.urls import reverse_lazy


def is_admin(user):
    return user.is_authenticated and user.is_staff


def custom_logout(request):
    logout(request)
    return render(request, 'registration/logout.html')


class CustomLoginView(LoginView):
    def get_success_url(self):
        user = self.request.user

        if user.is_staff:
            return reverse_lazy('website:lista_master')
        else:
            pass


@user_passes_test(is_admin)
def lista_master(request):
    masters = MasterIgrometri.objects.all()
    return render(request, 'masters_list.html', {'masters': masters})


def mappa_aree(request):
    return render(request, 'mappa.html', {'sensors': read_and_average()})


def read_and_average():
    # Ottenere tutti i dati degli igrometri
    igrometri = Igrometro.objects.all()

    # Definire le dimensioni del rettangolo
    lat_delta = 0.01
    lon_delta = 0.01

    # Creare una lista per i dati medi dei rettangoli
    rettangoli_dati_medi = []

    # Iterare sugli igrometri
    rettangoli = []
    for igrometro in igrometri:
        # Calcolare i limiti del rettangolo basandosi sulla posizione dell'igrometro
        lat_start = int(igrometro.latitudine / lat_delta) * lat_delta
        lat_end = lat_start + lat_delta
        lon_start = int(igrometro.longitudine / lon_delta) * lon_delta
        lon_end = lon_start + lon_delta

        # Creare il poligono del rettangolo
        rettangolo = {"lat_start": lat_start, "lon_start": lon_start, "lat_end": lat_end, "lon_end": lon_end}
        if rettangolo in rettangoli:
            continue
        else:
            rettangoli.append(rettangolo)

        # Filtrare gli igrometri all'interno del rettangolo
        igrometri_in_rettangolo = igrometri.filter(latitudine__range=(lat_start, lat_end),
                                                   longitudine__range=(lon_start, lon_end))

        if igrometri_in_rettangolo.exists():
            media_valori = sum(i.ultima_misurazione["valore"] for i in igrometri_in_rettangolo) / len(
                igrometri_in_rettangolo)

            rettangoli_dati_medi.append({
                'latitudine_start': str(lat_start),
                'latitudine_end': str(lat_end),
                'longitudine_start': str(lon_start),
                'longitudine_end': str(lon_end),
                'media_valori': str(media_valori),
            })

    return rettangoli_dati_medi
