# Create your views here.
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Cliente, Ventas, DetalleVenta, Usuario, Reparto

@login_required(login_url='login')
def lista_ventas(request):
    ventas = Ventas.objects.all()
    return render(request, 'reparto/lista_ventas.html', {
        'ventas': ventas
    })

@login_required(login_url='login')  
def cliente(request):
    clientes = Cliente.objects.select_related('cliente').all().order_by('-fecha')
    return render(request, 'reparto/cliente.html', {
        'clientes': clientes
    })

@login_required(login_url='login')
def boletas_por_gasto(request, gasto_id):
    gasto = get_object_or_404(GastosComunes, id=gasto_id)
    boletas = BoletaGC.objects.filter(gastosComunes=gasto).order_by('-fecha')
    return render(request, 'gastos_comunes/detalle_boleta.html', {
        'gasto': gasto,
        'boletas': boletas
    })

@login_required(login_url='login')
def reparto(request):
    cliente = Cliente.objects.count()
    usuario = Usuario.objects.count()
    ventas = Ventas.objects.select_related('reparto').order_by('-estado')[:5]
    
    return render(request, 'reparto/reparto.html', {
        'cliente': cliente,
        'usuario': usuario,
        'ventas': ventas
    })