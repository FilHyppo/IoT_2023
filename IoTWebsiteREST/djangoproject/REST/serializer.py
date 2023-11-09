from rest_framework import serializers
from .models import Idrometro, MasterIdrometri

class MasterIdrometriSerializer(serializers.ModelSerializer):
    class Meta:
        model = MasterIdrometri
        fields = ['id', 'nome', 'latitudine', 'longitudine', 'quota']

class IdrometroSerializer(serializers.ModelSerializer):
    master_id = serializers.PrimaryKeyRelatedField(queryset=MasterIdrometri.objects.all(), source='master', write_only=True)

    class Meta:
        model = Idrometro
        fields = ['id', 'nome', 'latitudine', 'longitudine', 'ultima_misurazione', 'master_id']