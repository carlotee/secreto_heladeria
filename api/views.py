from django.http import JsonResponse
from rest_framework import viewsets
from centro_costos.models import TipoCosto, Costo
from .serializers import TipoCostoSerializer, CostoSerializer
from rest_framework.permissions import IsAuthenticated


def health(request):
    return JsonResponse({"status": "ok"})

def info_api(request):
    data = {
        "proyecto": "Secreto Heladeria API",
        "version": "1.0",
        "autor": "Carlos"
    }
    return JsonResponse(data)

class TipoCostoViewSet(viewsets.ModelViewSet):
    queryset = TipoCosto.objects.all()
    serializer_class = TipoCostoSerializer
    permission_classes = [IsAuthenticated]   # 👈 protección activada


class CostoViewSet(viewsets.ModelViewSet):
    queryset = Costo.objects.all()
    serializer_class = CostoSerializer
    permission_classes = [IsAuthenticated]   # 👈 protección activada
