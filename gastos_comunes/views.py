# Create your views here.
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import GastosComunes, BoletaGC

@login_required(login_url='login')
def gastos_comunes_lista(request):
    gastos = GastosComunes.objects.all()
    return render(request, 'gastos_comunes/gc_lista.html', {
        'gastos': gastos
    })

@login_required(login_url='login')  
def boletas_lista(request):
    boletas = BoletaGC.objects.select_related('gastosComunes').all().order_by('-fecha')
    return render(request, 'gastos_comunes/boletas_lista.html', {
        'boletas': boletas
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
def gastos_comunes(request):
    total_gastos = GastosComunes.objects.count()
    total_boletas = BoletaGC.objects.count()
    ultimas_boletas = BoletaGC.objects.select_related('gastosComunes').order_by('-fecha')[:5]
    
    return render(request, 'gastos_comunes/gastos_comunes.html', {
        'total_gastos': total_gastos,
        'total_boletas': total_boletas,
        'ultimas_boletas': ultimas_boletas
    })