from rest_framework import serializers
from .models import Igrometro, MasterIgrometri

class MasterIgrometriSerializer(serializers.ModelSerializer):
    class Meta:
        model = MasterIgrometri
        fields = ['id', 'nome', 'latitudine', 'longitudine', 'quota']

class IgrometroSerializer(serializers.ModelSerializer):
    master_id = serializers.PrimaryKeyRelatedField(queryset=MasterIgrometri.objects.all(), source='master', write_only=True)

    class Meta:
        model = Igrometro
        fields = ['id', 'nome', 'latitudine', 'longitudine', 'ultima_misurazione', 'master_id']


