from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.db.models import Q, Sum
from .models import Periodo, TipoCosto, Centro_Costos, Costo
from .forms import PeriodoForm, TipoCostoForm, CentroCostosForm, CostoForm, ConfirmarEliminarCostoForm
from proveedores.models import Proveedor


def periodo(request):
    periodos = Periodo.objects.all().order_by('-año', '-mes')
    return render(request, 'centro_costos/periodo.html', {'periodos': periodos})


def periodo_crear(request):
    if request.method == 'POST':
        form = PeriodoForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Periodo creado exitosamente')
            return redirect('periodo')
        else:
            messages.error(request, 'Revisa los campos e intenta nuevamente')
    else:
        form = PeriodoForm()

    return render(request, 'centro_costos/periodo_crear.html', {'form': form})


def periodo_act(request, pk):
    periodo = get_object_or_404(Periodo, pk=pk)

    if request.method == 'POST':
        form = PeriodoForm(request.POST, instance=periodo)
        if form.is_valid():
            form.save()
            messages.success(request, 'Periodo actualizado exitosamente')
            return redirect('periodo')
    else:
        form = PeriodoForm(instance=periodo)

    return render(request, 'centro_costos/periodo_act.html', {'form': form, 'periodo': periodo})


def periodo_eliminar(request, pk):
    periodo = get_object_or_404(Periodo, pk=pk)

    if request.method == 'POST':
        periodo.delete()
        messages.success(request, 'Periodo eliminado exitosamente')
        return redirect('periodo')

    return render(request, 'centro_costos/periodo_eliminar.html', {'periodo': periodo})



def tipo_costo(request):
    tipos = TipoCosto.objects.all()
    return render(request, 'centro_costos/tipo_costo.html', {'tipos': tipos})



def centro_costos(request):
    centros = Centro_Costos.objects.filter(deleted_at__isnull=True).order_by('-created_at')
    return render(request, 'centro_costos/centro_costos.html', {'centros': centros})



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
        form = CostoForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Costo creado exitosamente')
            return redirect('costo')
        else:
            messages.error(request, 'Verifica los campos e intenta nuevamente')
    else:
        form = CostoForm()

    return render(request, 'centro_costos/costo_crear.html', {'form': form})


def costo_act(request, pk):
    costo = get_object_or_404(Costo, pk=pk)

    if request.method == 'POST':
        form = CostoForm(request.POST, instance=costo)
        if form.is_valid():
            form.save()
            messages.success(request, 'Costo actualizado exitosamente')
            return redirect('costo')
        else:
            messages.error(request, 'Error al actualizar el costo')
    else:
        form = CostoForm(instance=costo)

    return render(request, 'centro_costos/costo_act.html', {'form': form, 'costo': costo})


def costo_eliminar(request, pk):
    costo = get_object_or_404(Costo, pk=pk)

    if request.method == 'POST':
            costo.delete()
            messages.success(request, 'Costo eliminado exitosamente')
            return redirect('costo')

    return render(request, 'centro_costos/costo_eliminar.html', {'costo': costo})


@login_required
def dashboard(request):
    centros = Centro_Costos.objects.prefetch_related('costo_set__periodo', 'tipo_costo')

    centros_con_periodos = []
    for centro in centros:
        costos = centro.costo_set.all()
        periodos = (
            Periodo.objects
            .filter(costo__centro_costo=centro)
            .distinct()
            .order_by('-año', '-mes')
        )

        centros_con_periodos.append({
            'centro': centro,
            'costos': costos,
            'periodos': periodos,
        })

    ultimo_periodo = Periodo.objects.order_by('-año', '-mes').first()
    costos_recientes = (
        Costo.objects.filter(periodo=ultimo_periodo).aggregate(total=Sum('valor'))['total']
        if ultimo_periodo else 0
    )
    
    proveedores = Proveedor.objects.all()

    context = {
        'centros_con_periodos': centros_con_periodos,
        'ultimo_periodo': ultimo_periodo,
        'costos_recientes': costos_recientes,
        'total_centros': Centro_Costos.objects.filter(deleted_at__isnull=True).count(),
        'total_tipos': TipoCosto.objects.count(),
        'proveedores': proveedores,
    }

    return render(request, 'centro_costos/dashboard.html', context)