from django.contrib import admin
from .models import Igrometro, MasterIgrometri, Irrigatore, CustomUser

# Register your models here.


class MasterIgrometriAdmin(admin.ModelAdmin):
    list_display = ('id', 'nome', 'latitudine', 'longitudine', 'data_creazione', 'quota')

class IgrometroAdmin(admin.ModelAdmin):
    list_display = ('id', 'nome', 'latitudine', 'longitudine', 'data_creazione', 'ultima_misurazione', 'attivo', 'master')

admin.site.register(MasterIgrometri, MasterIgrometriAdmin)
admin.site.register(Igrometro, IgrometroAdmin)
admin.site.register(CustomUser)
admin.site.register(Irrigatore)
