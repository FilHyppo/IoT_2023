from django.contrib.auth import logout
from django.contrib.auth.views import LoginView
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.decorators import user_passes_test
from django.views import View
from .forms import IgrometroForm, IrrigatoreForm, MasterForm
from REST.models import Igrometro, MasterIgrometri
from django.urls import reverse_lazy
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator

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


#@user_passes_test(is_admin)
def lista_master(request):
    masters = MasterIgrometri.objects.all()
    return render(request, 'masters_list.html', {'masters': masters})


def mappa_aree(request):
    return render(request, 'mappa.html', {'sensors': read_and_average()})

def homepage(request):
    return render(request, 'homepage.html', )

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
            media_valori = sum(i.ultima_misurazione["umidita"] for i in igrometri_in_rettangolo) / len(
                igrometri_in_rettangolo)

            rettangoli_dati_medi.append({
                'latitudine_start': str(lat_start),
                'latitudine_end': str(lat_end),
                'longitudine_start': str(lon_start),
                'longitudine_end': str(lon_end),
                'media_valori': str(media_valori),
            })

    return rettangoli_dati_medi

@method_decorator(login_required, name='dispatch')
class AggiungiIrrigatoreView(View):
    template_name = 'aggiungi_irrigatore.html'

    def get(self, request):
        form = IrrigatoreForm()
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = IrrigatoreForm(request.POST)
        if form.is_valid():
            irrigatore = form.save(commit=False)
            irrigatore.user = request.user  # Associa l'irrigatore all'utente corrente
            irrigatore.save()
            return redirect('website:lista_master')  # Personalizza l'URL di reindirizzamento

        return render(request, self.template_name, {'form': form})


# views.py
from django.http import JsonResponse
from django.views import View

from django.http import JsonResponse
from django.views import View


class MasterIgrometriSearchView(View):
    def get(self, request, *args, **kwargs):
        search_name = request.GET.get('searchName', '')
        type = request.GET.get('type', '')
        id = request.GET.get('id', '')


        masters_queryset = MasterIgrometri.objects.all()
        igrometri_queryset = Igrometro.objects.all()
        if id:
            try:
                id = int(id)
                master_instance = MasterIgrometri.objects.get(id=id)
                masters_queryset = [master_instance]
            except (ValueError, MasterIgrometri.DoesNotExist):
                masters_queryset = []
            try:
                id = int(id)
                igrometro_instance = Igrometro.objects.get(id=id)
                igrometri_queryset = [igrometro_instance]
            except (ValueError, MasterIgrometri.DoesNotExist):
                igrometri_queryset = []




        if type == "Master":
            igrometri_queryset = []
            
        elif type == "Hygrometer":
            masters_queryset = []

    
        if search_name:
            masters_queryset = [master for master in masters_queryset if search_name.lower() in master.nome.lower()]
            igrometri_queryset = [igro for igro in igrometri_queryset if search_name.lower() in igro.nome.lower()]

        masters_data = []
        for master in masters_queryset:
            master_data = {
                'id': master.id,
                'nome': master.nome,
                'latitudine': master.latitudine,
                'longitudine': master.longitudine,
                'data_creazione': master.data_creazione,
                'quota': master.quota,
            }
            masters_data.append(master_data)

        igrometri_data = []
        for igrometro in igrometri_queryset:
            igrometro_data = {
                'id': igrometro.id,
                'nome': igrometro.nome,
                'latitudine': igrometro.latitudine,
                'longitudine': igrometro.longitudine,
                'data_creazione': igrometro.data_creazione,
                'ultima_misurazione': igrometro.ultima_misurazione,
                'misurazioni': igrometro.misurazioni,
                'attivo': igrometro.attivo,
                'master_id': igrometro.master_id,
            }
            igrometri_data.append(igrometro_data)

        result_dict = {
            'masters': masters_data,
            'igrometri': igrometri_data
        }
        return JsonResponse(result_dict, safe=False)
    

def igrometro_detail_and_edit(request, igrometro_id):
    igrometro = get_object_or_404(Igrometro, id=igrometro_id)
    if request.method == 'POST':
        form = IgrometroForm(request.POST, instance=igrometro)
        if form.is_valid():
            form.save()
            return render(request, 'igrometro.html', {'igrometro': igrometro, 'form': form})
    else:
        form = IgrometroForm(instance=igrometro)

    return render(request, 'igrometro.html', {'igrometro': igrometro, 'form': form})


def master_detail_and_edit(request, master_id):
    master = get_object_or_404(MasterIgrometri, id=master_id)
    igrometri = Igrometro.objects.filter(master=master)
    print(igrometri)
    if request.method == 'POST':
        form = MasterForm(request.POST, instance=master)
        if form.is_valid():
            form.save()
            return render(request, 'master.html', {'master': master, 'form': form , 'igrometri':igrometri})
    else:
        form = MasterForm(instance=master)

    return render(request, 'master.html', {'master': master, 'form': form, 'igrometri':igrometri})

