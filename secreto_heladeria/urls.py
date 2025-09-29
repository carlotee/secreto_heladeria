"""
URL configuration for secreto_heladeria project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include   
from accounts import views as accounts_views
from organizations import views as org_views
from produccion import views as pro_views
from gastos_comunes import views as gc_views
from reparto import views as rep_views


urlpatterns = [
    path('admin/', admin.site.urls),
    path("dashboard/", org_views.dashboard, name="dashboard"),
    path('registro/', accounts_views.registro, name='registro'),
    path('login/', accounts_views.login_view, name='login'),
    path('productos/', pro_views.producto_lista, name='producto_lista'),
    path('productos/<int:id>/', pro_views.detalle_compra, name='detalle_compra'),
    path('gastos_comunes/', gc_views.gastos_comunes, name='gastos_comunes'),
    path('reparto/', rep_views.reparto, name='reparto'),
]
