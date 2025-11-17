from django.urls import path
from .views import health
from .views import info_api

urlpatterns = [
        path('health/', health),
        path("info/", info_api),
]
