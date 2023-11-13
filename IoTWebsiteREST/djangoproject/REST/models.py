import datetime
from django.db import models

PARAMS = ['data', 'umidita'] #parametri che ogni misurazione dovrebbe contenere


# Create your models here.
class Igrometro(models.Model):
    id = models.AutoField(primary_key=True)
    nome = models.CharField(max_length=100)
    latitudine = models.FloatField()
    longitudine = models.FloatField()
    data_creazione = models.DateTimeField(auto_now_add=True, blank=True, null=True)


    ultima_misurazione = models.JSONField(default=dict, blank=True, null=True)
    misurazioni = models.JSONField(default=list, blank=True, null=True)


    attivo = models.BooleanField(default=False)
    master = models.ForeignKey('MasterIgrometri', on_delete=models.CASCADE, null=True)
    def __str__(self):
        return self.nome
    
class MasterIgrometri(models.Model):
    id = models.AutoField(primary_key=True)
    nome = models.CharField(max_length=100)
    latitudine = models.FloatField()
    longitudine = models.FloatField()
    data_creazione = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    quota = models.FloatField()
    def __str__(self):
        return self.nome