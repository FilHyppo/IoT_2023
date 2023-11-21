from rest_framework import serializers
from .models import Igrometro, MasterIgrometri, CustomUser
from rest_framework.authtoken.models import Token
from django.contrib.auth import get_user_model

class MasterIgrometriSerializer(serializers.ModelSerializer):
    class Meta:
        model = MasterIgrometri
        fields = ['id', 'nome', 'latitudine', 'longitudine', 'quota']

class IgrometroSerializer(serializers.ModelSerializer):
    master_id = serializers.PrimaryKeyRelatedField(queryset=MasterIgrometri.objects.all(), source='master', write_only=True)

    class Meta:
        model = Igrometro
        fields = ['id', 'nome', 'latitudine', 'longitudine', 'ultima_misurazione', 'master_id']

class TokenSerializer(serializers.ModelSerializer):
    class Meta:
        model = Token
        fields = ('key', 'user')

class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ('id', 'username', 'email')