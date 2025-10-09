from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.db.models import Q, Sum
from .models import Periodo, TipoCosto, Centro_Costos, Costo

<<<<<<< HEAD
# ==================== PERIODO ====================

def periodo(request):
    """Lista todos los periodos"""
    periodos = Periodo.objects.all().order_by('-año', '-mes')
    context = {
        'periodos': periodos
    }
    return render(request, 'centro_costos/periodo.html', context)

def periodo_crear(request):
    """Crear nuevo periodo"""
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
    """Actualizar periodo existente"""
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


# ==================== TIPO COSTO ====================

def tipo_costo(request):
    """Lista todos los tipos de costo"""
    tipos = TipoCosto.objects.all()
    context = {
        'tipos': tipos
    }
    return render(request, 'centro_costos/tipo_costo.html', context)

def tipo_costo_crear(request):
    """Crear nuevo tipo de costo"""
    if request.method == 'POST':
        nombre = request.POST.get('nombre')
        
        if nombre:
            TipoCosto.objects.create(nombre=nombre)
            messages.success(request, 'Tipo de costo creado exitosamente')
            return redirect('tipo_costo')
        else:
            messages.error(request, 'El nombre es obligatorio')
    
    return render(request, 'centro_costos/tipo_costo_crear.html')

def tipo_costo_act(request, pk):
    """Actualizar tipo de costo"""
    tipo = get_object_or_404(TipoCosto, pk=pk)
    
    if request.method == 'POST':
        tipo.nombre = request.POST.get('nombre')
        tipo.save()
        messages.success(request, 'Tipo de costo actualizado exitosamente')
        return redirect('tipo_costo')
    
    context = {'tipo': tipo}
    return render(request, 'centro_costos/tipo_costo_act.html', context)

def tipo_costo_elim(request, pk):
    """Eliminar tipo de costo"""
    tipo = get_object_or_404(TipoCosto, pk=pk)
    
    if request.method == 'POST':
        tipo.delete()
        messages.success(request, 'Tipo de costo eliminado exitosamente')
        return redirect('tipo_costo')
    
    context = {'tipo': tipo}
    return render(request, 'centro_costos/tipo_costo_confirm_elim.html', context)


# ==================== CENTRO DE COSTOS ====================

def centro_costos(request):
    """Lista todos los centros de costos (excluyendo eliminados)"""
    centros = Centro_Costos.objects.filter(deleted_at__isnull=True).order_by('-created_at')
    context = {
        'centros': centros
    }
    return render(request, 'centro_costos/centro_costos.html', context)

def centro_costos_crear(request):
    """Crear nuevo centro de costos"""
    if request.method == 'POST':
        nombre = request.POST.get('nombre')
        tipo_costo = request.POST.get('tipo_costo')
        
        if nombre and tipo_costo:
            Centro_Costos.objects.create(
                nombre=nombre,
                tipo_costo=tipo_costo
            )
            messages.success(request, 'Centro de costos creado exitosamente')
            return redirect('centro_costos')
        else:
            messages.error(request, 'Todos los campos son obligatorios')
    
    context = {
        'tipo_choices': Centro_Costos.TIPO_COSTO_CHOICES
    }
    return render(request, 'centro_costos/centro_costos_crear.html', context)

def centro_costos_act(request, pk):
    """Actualizar centro de costos"""
    centro = get_object_or_404(Centro_Costos, pk=pk, deleted_at__isnull=True)
    
    if request.method == 'POST':
        centro.nombre = request.POST.get('nombre')
        centro.tipo_costo = request.POST.get('tipo_costo')
        centro.save()
        messages.success(request, 'Centro de costos actualizado exitosamente')
        return redirect('centro_costos')
    
    context = {
        'centro': centro,
        'tipo_choices': Centro_Costos.TIPO_COSTO_CHOICES
    }
    return render(request, 'centro_costos/centro_costos_act.html', context)

def centro_costos_elim(request, pk):
    """Eliminación lógica de centro de costos"""
    from django.utils import timezone
    centro = get_object_or_404(Centro_Costos, pk=pk, deleted_at__isnull=True)
    
    if request.method == 'POST':
        centro.deleted_at = timezone.now()
        centro.save()
        messages.success(request, 'Centro de costos eliminado exitosamente')
        return redirect('centro_costos')
    
    context = {'centro': centro}
    return render(request, 'centro_costos/centro_costos_confirm_elim.html', context)


# ==================== COSTO ====================

def costo(request):
    """Lista todos los costos con filtros"""
    costos = Costo.objects.select_related('tipo_costo', 'centro_costo', 'periodo').all()
    
    # Filtros
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
    
    # Total de costos
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
    """Crear nuevo costo"""
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
    """Actualizar costo existente"""
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
    """Eliminar costo"""
    costo = get_object_or_404(Costo, pk=pk)
    
    if request.method == 'POST':
        costo.delete()
        messages.success(request, 'Costo eliminado exitosamente')
        return redirect('costo')
    
    context = {'costo': costo}
    return render(request, 'centro_costos/costo_eliminar.html', context)


# ==================== REPORTES Y DASHBOARD ====================

def dashboard(request):
    """Dashboard con resumen de costos"""
    from django.db.models import Count
    
    # Total de costos por tipo
    costos_por_tipo = Costo.objects.values('tipo_costo__nombre').annotate(
        total=Sum('valor'),
        cantidad=Count('id')
    )
    
    # Total de costos por centro
    costos_por_centro = Costo.objects.filter(
        centro_costo__isnull=False
    ).values('centro_costo__nombre', 'centro_costo__tipo_costo').annotate(
        total=Sum('valor')
    )
    
    # Costos del último periodo
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
    """Reporte detallado por periodo"""
    periodo = get_object_or_404(Periodo, pk=periodo_id)
    costos = Costo.objects.filter(periodo=periodo).select_related(
        'tipo_costo', 'centro_costo'
    )
    
    # Totales
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
=======
# Create your views here.
def centro_costos_view(request):
    return render(request, 'centro_costos/centro_costos.html')

def costo(request, id):
    return render(request, 'centro_costos/costo.html', {'id': id})

def tipo_costo(request):
    return render(request, 'centro_costos/tipo_costo.html')
>>>>>>> main
