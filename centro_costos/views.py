from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.db.models import Q, Sum
from .models import Periodo, TipoCosto, Centro_Costos, Costo

def periodo(request):
    periodos = Periodo.objects.all().order_by('-año', '-mes')
    context = {
        'periodos': periodos
    }
    return render(request, 'centro_costos/periodo.html', context)

def periodo_crear(request):
    if request.method == 'POST':
        año = request.POST.get('año')
        mes = request.POST.get('mes')
        
        if año and mes:
            Periodo.objects.create(año=año, mes=mes)
            messages.success(request, 'Periodo creado exitosamente')
            return redirect('periodo')
        else:
            messages.error(request, 'Todos los campos son obligatorios')
    
    return render(request, 'centro_costos/periodo_crear.html')

def periodo_act(request, pk):
    periodo = get_object_or_404(Periodo, pk=pk)
    
    if request.method == 'POST':
        periodo.año = request.POST.get('año')
        periodo.mes = request.POST.get('mes')
        periodo.save()
        messages.success(request, 'Periodo actualizado exitosamente')
        return redirect('periodo')
    
    context = {'periodo': periodo}
    return render(request, 'centro_costos/periodo_act.html', context)

def periodo_eliminar(request, pk):
    """Eliminar periodo"""
    periodo = get_object_or_404(Periodo, pk=pk)
    
    if request.method == 'POST':
        periodo.delete()
        messages.success(request, 'Periodo eliminado exitosamente')
        return redirect('periodo')
    
    context = {'periodo': periodo}
    return render(request, 'centro_costos/periodo_confirm_eliminar.html', context)


def tipo_costo(request):
    tipos = TipoCosto.objects.all()
    context = {
        'tipos': tipos
    }
    return render(request, 'centro_costos/tipo_costo.html', context)


def centro_costos(request):
    """Lista todos los centros de costos (excluyendo eliminados)"""
    centros = Centro_Costos.objects.filter(deleted_at__isnull=True).order_by('-created_at')
    context = {
        'centros': centros
    }
    return render(request, 'centro_costos/centro_costos.html', context)



def costo(request):
    costos = Costo.objects.select_related('tipo_costo', 'centro_costo', 'periodo').all()
    
    periodo_id = request.GET.get('periodo')
    tipo_id = request.GET.get('tipo')
    centro_id = request.GET.get('centro')
    search = request.GET.get('search')
    
    if periodo_id:
        costos = costos.filter(periodo_id=periodo_id)
    if tipo_id:
        costos = costos.filter(tipo_costo_id=tipo_id)
    if centro_id:
        costos = costos.filter(centro_costo_id=centro_id)
    if search:
        costos = costos.filter(
            Q(descripcion__icontains=search) | 
            Q(tipo_costo__nombre__icontains=search)
        )
    
    total = costos.aggregate(total=Sum('valor'))['total'] or 0
    
    context = {
        'costos': costos,
        'total': total,
        'periodos': Periodo.objects.all(),
        'tipos': TipoCosto.objects.all(),
        'centros': Centro_Costos.objects.filter(deleted_at__isnull=True),
    }
    return render(request, 'centro_costos/costo.html', context)

def costo_crear(request):
    if request.method == 'POST':
        descripcion = request.POST.get('descripcion')
        valor = request.POST.get('valor')
        tipo_costo_id = request.POST.get('tipo_costo')
        centro_costo_id = request.POST.get('centro_costo')
        periodo_id = request.POST.get('periodo')
        
        if descripcion and valor and tipo_costo_id and periodo_id:
            Costo.objects.create(
                descripcion=descripcion,
                valor=valor,
                tipo_costo_id=tipo_costo_id,
                centro_costo_id=centro_costo_id if centro_costo_id else None,
                periodo_id=periodo_id
            )
            messages.success(request, 'Costo creado exitosamente')
            return redirect('costo')
        else:
            messages.error(request, 'Los campos descripción, valor, tipo y periodo son obligatorios')
    
    context = {
        'tipos': TipoCosto.objects.all(),
        'centros': Centro_Costos.objects.filter(deleted_at__isnull=True),
        'periodos': Periodo.objects.all().order_by('-año', '-mes')
    }
    return render(request, 'centro_costos/costo_crear.html', context)

def costo_act(request, pk):
    costo = get_object_or_404(Costo, pk=pk)
    
    if request.method == 'POST':
        costo.descripcion = request.POST.get('descripcion')
        costo.valor = request.POST.get('valor')
        costo.tipo_costo_id = request.POST.get('tipo_costo')
        centro_costo_id = request.POST.get('centro_costo')
        costo.centro_costo_id = centro_costo_id if centro_costo_id else None
        costo.periodo_id = request.POST.get('periodo')
        costo.save()
        messages.success(request, 'Costo actualizado exitosamente')
        return redirect('costo')
    
    context = {
        'costo': costo,
        'tipos': TipoCosto.objects.all(),
        'centros': Centro_Costos.objects.filter(deleted_at__isnull=True),
        'periodos': Periodo.objects.all().order_by('-año', '-mes')
    }
    return render(request, 'centro_costos/costo_act.html', context)

def costo_eliminar(request, pk):
    costo = get_object_or_404(Costo, pk=pk)
    
    if request.method == 'POST':
        costo.delete()
        messages.success(request, 'Costo eliminado exitosamente')
        return redirect('costo')
    
    context = {'costo': costo}
    return render(request, 'centro_costos/costo_eliminar.html', context)


@login_required
def dashboard(request):
    from django.db.models import Count
    
    costos_por_tipo = Costo.objects.values('tipo_costo__nombre').annotate(
        total=Sum('valor'),
        cantidad=Count('id')
    )
    
    costos_por_centro = Costo.objects.filter(
        centro_costo__isnull=False
    ).values('centro_costo__nombre', 'centro_costo__tipo_costo').annotate(
        total=Sum('valor')
    )
    
    ultimo_periodo = Periodo.objects.order_by('-año', '-mes').first()
    costos_recientes = None
    if ultimo_periodo:
        costos_recientes = Costo.objects.filter(
            periodo=ultimo_periodo
        ).aggregate(total=Sum('valor'))['total'] or 0
    
    context = {
        'costos_por_tipo': costos_por_tipo,
        'costos_por_centro': costos_por_centro,
        'costos_recientes': costos_recientes,
        'ultimo_periodo': ultimo_periodo,
        'total_centros': Centro_Costos.objects.filter(deleted_at__isnull=True).count(),
        'total_tipos': TipoCosto.objects.count(),
    }
    return render(request, 'centro_costos/dashboard.html', context)

def reporte_periodo(request, periodo_id):
    periodo = get_object_or_404(Periodo, pk=periodo_id)
    costos = Costo.objects.filter(periodo=periodo).select_related(
        'tipo_costo', 'centro_costo'
    )
    
    total_general = costos.aggregate(total=Sum('valor'))['total'] or 0
    total_fijos = costos.filter(centro_costo__tipo_costo='Fijo').aggregate(
        total=Sum('valor')
    )['total'] or 0
    total_variables = costos.filter(centro_costo__tipo_costo='Variable').aggregate(
        total=Sum('valor')
    )['total'] or 0
    
    context = {
        'periodo': periodo,
        'costos': costos,
        'total_general': total_general,
        'total_fijos': total_fijos,
        'total_variables': total_variables,
    }
    return render(request, 'centro_costos/reporte_periodo.html', context)