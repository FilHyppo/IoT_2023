from django.shortcuts import render
from django.contrib.auth.decorators import user_passes_test
from REST.models import Igrometro, MasterIgrometri

def is_admin(user):
    return user.is_authenticated and user.is_staff


@user_passes_test(is_admin)
def lista_master(request):
    masters = MasterIgrometri.objects.all()
    return render(request, 'masters_list.html', {'masters': masters})