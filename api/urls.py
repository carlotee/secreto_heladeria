from django.urls import path,include
from rest_framework import routers
from .views import TipoCostoViewSet, CostoViewSet
from .views import info_api, health

router = routers.DefaultRouter()
router.register(r'tipocosto',TipoCostoViewSet)
router .register(r'costo',CostoViewSet)

urlpatterns = [
        path('health/', health),
        path("info/", info_api),
        path('', include(router.urls)),
]
