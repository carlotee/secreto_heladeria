from django.urls import path,include
from rest_framework import routers
from .views import TipoCostoViewSet, CostoViewSet
from .views import info_api, health
from rest_framework.authtoken.views import obtain_auth_token

router = routers.DefaultRouter()
router.register(r'tipocosto',TipoCostoViewSet)
router .register(r'costo',CostoViewSet)

urlpatterns = [
        path('health/', health),
        path("info/", info_api),
        path('', include(router.urls)),
        path('api/login/', obtain_auth_token, name='api_login'),

]
