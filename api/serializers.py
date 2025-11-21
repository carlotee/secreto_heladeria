from rest_framework import serializers
from centro_costos.models import TipoCosto, Costo

class TipoCostoSerializer(serializers.ModelSerializer):
    class Meta:
        model = TipoCosto
        fields = '__all__'

class CostoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Costo
        fields = '__all__'