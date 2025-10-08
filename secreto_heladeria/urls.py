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
from centro_costos import views
from django.urls import path
from produccion import views as produccion_views
from proveedores import views as proveedores_views

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('periodos/', views.periodo, name='periodo'),
    path('periodos/crear/', views.periodo_crear, name='periodo_crear'),
    path('periodos/<int:pk>/editar/', views.periodo_act, name='periodo_act'),
    path('periodos/<int:pk>/eliminar/', views.periodo_eliminar, name='periodo_eliminar'),
    path('tipos-costo/', views.tipo_costo, name='tipo_costo'),
    path('tipos-costo/crear/', views.tipo_costo_crear, name='tipo_costo_crear'),
    path('tipos-costo/<int:pk>/editar/', views.tipo_costo_act, name='tipo_costo_act'),
    path('tipos-costo/<int:pk>/eliminar/', views.tipo_costo_elim, name='tipo_costo_elim'),
    path('centros-costos/', views.centro_costos, name='centro_costos'),
    path('centros-costos/crear/', views.centro_costos_crear, name='centro_costos_crear'),
    path('centros-costos/<int:pk>/editar/', views.centro_costos_act, name='centro_costos_act'),
    path('centros-costos/<int:pk>/eliminar/', views.centro_costos_elim, name='centro_costos_elim'),
    path('costos/', views.costo, name='costo'),
    path('costos/crear/', views.costo_crear, name='costo_crear'),
    path('costos/<int:pk>/editar/', views.costo_act, name='costo_act'),
    path('costos/<int:pk>/eliminar/', views.costo_eliminar, name='costo_eliminar'),
    path('reportes/periodo/<int:periodo_id>/', views.reporte_periodo, name='reporte_periodo'),
    path('', produccion_views.producto, name='producto'),
    path('crear/', produccion_views.producto_crear, name='producto_crear'),
    path('<int:pk>/', produccion_views.producto_detalle, name='producto_detalle'),
    path('<int:pk>/editar/', produccion_views.producto_act, name='producto_act'),
    path('<int:pk>/eliminar/', produccion_views.producto_eliminar, name='producto_eliminar'),
    path('', proveedores_views.proveedor, name='proveedor'),
    path('crear/', proveedores_views.proveedor_crear, name='proveedor_crear'),
    path('<int:pk>/', proveedores_views.proveedor_detalle, name='proveedor_detalle'),
    path('<int:pk>/editar/', proveedores_views.proveedor_act, name='proveedor_act'),
    path('<int:pk>/eliminar/', proveedores_views.proveedor_eliminar, name='proveedor_eliminar'),
]