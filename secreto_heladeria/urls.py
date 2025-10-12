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
from centro_costos import views as centro_costos_views
from produccion import views as produccion_views
from proveedores import views as proveedores_views

urlpatterns = [
    path('', centro_costos_views.dashboard, name='dashboard'),
    path('admin/', admin.site.urls),
    path('accounts/', include('django.contrib.auth.urls')),
    path('accounts/registro/', accounts_views.registro, name='registro'),
    path('login/', accounts_views.login_view, name='login'),
    path('periodos/', centro_costos_views.periodo, name='periodo'),
    path('periodos/crear/', centro_costos_views.periodo_crear, name='periodo_crear'),
    path('periodos/<int:pk>/editar/', centro_costos_views.periodo_act, name='periodo_act'),
    path('periodos/<int:pk>/eliminar/', centro_costos_views.periodo_eliminar, name='periodo_eliminar'),
    path('tipos-costo/', centro_costos_views.tipo_costo, name='tipo_costo'),
    path('centros-costos/', centro_costos_views.centro_costos, name='centro_costos'),
    path('costos/', centro_costos_views.costo, name='costo'),
    path('costos/crear/', centro_costos_views.costo_crear, name='costo_crear'),
    path('costos/<int:pk>/editar/', centro_costos_views.costo_act, name='costo_act'),
    path('costos/<int:pk>/eliminar/', centro_costos_views.costo_eliminar, name='costo_eliminar'),
    path('', produccion_views.producto, name='producto'),
    path('crear/', produccion_views.producto_crear, name='producto_crear'),##
    path('<int:pk>/', produccion_views.producto_detalle, name='producto_detalle'),
    path('<int:pk>/editar/', produccion_views.producto_act, name='producto_act'),
    path('<int:pk>/eliminar/', produccion_views.producto_eliminar, name='producto_eliminar'),
    path('proveedores', proveedores_views.proveedor, name='proveedor'),
    path('proveedor/crear/', proveedores_views.proveedor_crear, name='proveedor_crear'),
    path('<int:pk>/', proveedores_views.proveedor_detalle, name='proveedor_detalle'),
    path('<int:pk>/editar/', proveedores_views.proveedor_act, name='proveedor_act'),
    path('<int:pk>/eliminar/', proveedores_views.proveedor_eliminar, name='proveedor_eliminar'),
    path('logout/', accounts_views.logout_view, name='logout'),
    path('proveedor/<int:proveedor_id>/dashboard/', proveedores_views.proveedor_dashboard, name='proveedor_dashboard'),
]
