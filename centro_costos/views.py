from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.db.models import Q, Sum
from .models import Periodo, TipoCosto, Centro_Costos, Costo, TransaccionCompra
from .forms import PeriodoForm, TipoCostoForm, CentroCostosForm, CostoForm, ConfirmarEliminarCostoForm, TransaccionCompraForm
from proveedores.models import Proveedor
from common.decorators_cost import rol_requerido_costos as rol_requerido
from common.decorators_pe import rol_requerido_pe
from openpyxl import Workbook
from django.http import HttpResponse
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from django.http import JsonResponse
from django.db import IntegrityError
import datetime
from django.utils import timezone

@login_required
def perfil_editar(request):
    if request.method == 'POST':
        user = request.user
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        
        user.first_name = first_name
        user.last_name = last_name
        user.email = email
        user.save()
        
        messages.success(request, 'Perfil actualizado exitosamente')
        return redirect('dashboard')
    
    return render(request, 'centro_costos/perfil_editar.html')

@login_required
def cambiar_contrasena(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  

            if request.headers.get('x-requested-with') == 'XMLHttpRequest':
                return JsonResponse({'success': True, 'redirect_url': '/'})

            messages.success(request, 'Contraseña cambiada exitosamente')
            return redirect('dashboard')
        else:
            errors = form.errors.get_json_data()
            if request.headers.get('x-requested-with') == 'XMLHttpRequest':
                return JsonResponse({'success': False, 'errors': errors})

            for field_errors in form.errors.values():
                for error in field_errors:
                    messages.error(request, error)
    else:
        form = PasswordChangeForm(request.user)

    return render(request, 'centro_costos/cambiar_contrasena.html', {'form': form})


def periodo(request):
    periodos = Periodo.objects.all().order_by('-año', '-mes')
    return render(request, 'centro_costos/periodo.html', {'periodos': periodos})

@login_required
@rol_requerido_pe('administrador')
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

@login_required
@rol_requerido_pe('administrador')
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

@login_required
@rol_requerido_pe('administrador')
def periodo_eliminar(request, pk):
    periodo = get_object_or_404(Periodo, pk=pk)

    if request.method == 'POST':
        periodo.delete()
        messages.success(request, 'Periodo eliminado exitosamente')
        return redirect('periodo')

    return render(request, 'centro_costos/periodo_eliminar.html', {'periodo': periodo})


@login_required
def tipo_costo(request):
    tipos = TipoCosto.objects.all()
    return render(request, 'centro_costos/tipo_costo.html', {'tipos': tipos})


@login_required
def centro_costos(request):
    centros = Centro_Costos.objects.filter(deleted_at__isnull=True).order_by('-created_at')
    return render(request, 'centro_costos/centro_costos.html', {'centros': centros})


@login_required
def costo(request):
    costos = Costo.objects.select_related('tipo_costo').all()
    costos = Costo.objects.all().order_by('id')

    tipo_id = request.GET.get('tipo')
    search = request.GET.get('search')

    if tipo_id:
        costos = costos.filter(tipo_costo_id=tipo_id)

    if search:
        costos = costos.filter(
            Q(descripcion__icontains=search) |
            Q(tipo_costo__nombre__icontains=search)
        )

    context = {
        'costos': costos,
        'tipos': TipoCosto.objects.all(),
    }

    return render(request, 'centro_costos/costo.html', context)

@login_required
@rol_requerido('administrador')
def costo_crear(request):
    if request.method == 'POST':
        form = CostoForm(request.POST)
        if form.is_valid():
            try:
                form.save()
                messages.success(request, 'Item Costo creado exitosamente')
                return redirect('costo')
            except IntegrityError:
                form.add_error(None, "Item Costo con esta Descripción y Categoría ya existe.")
        else:
            messages.error(request, 'Verifica los campos e intenta nuevamente')
    else:
        form = CostoForm()
    return render(request, 'centro_costos/costo_crear.html', {'form': form})

@login_required
@rol_requerido('administrador')
def costo_act(request, pk):
    costo = get_object_or_404(Costo, pk=pk)

    if request.method == 'POST':
        form = CostoForm(request.POST, instance=costo)
        if form.is_valid():
            form.save()
            messages.success(request, 'Item Costo actualizado exitosamente')
            return redirect('costo')
        else:
            messages.error(request, 'Error al actualizar el Item Costo')
    else:
        form = CostoForm(instance=costo)

    return render(request, 'centro_costos/costo_act.html', {'form': form, 'costo': costo})

@login_required
@rol_requerido('administrador')
def costo_eliminar(request, pk):
    costo = get_object_or_404(Costo, pk=pk)

    if request.method == 'POST':
            costo.delete()
            messages.success(request, 'Item Costo eliminado exitosamente')
            return redirect('costo')

    return render(request, 'centro_costos/costo_eliminar.html', {'costo': costo})

@login_required
def dashboard(request):
    centros = Centro_Costos.objects.select_related('tipo_costo')
    visitas = request.session.get('visitas', 0)
    request.session['visitas'] = visitas + 1

    centros_con_costos = []
    for centro in centros:
        costos = Costo.objects.filter(tipo_costo=centro.tipo_costo)
        centros_con_costos.append({
            'centro': centro,
            'costos': costos,
        })

    proveedores = Proveedor.objects.all()

    context = {
        'centros_con_costos': centros_con_costos,
        'total_centros': Centro_Costos.objects.filter(deleted_at__isnull=True).count(),
        'total_tipos': TipoCosto.objects.count(),
        'proveedores': proveedores,
        'visitas': visitas,
    }

    return render(request, 'centro_costos/dashboard.html', context)

def exportar_costos_excel(request):
    wb = Workbook()
    ws = wb.active
    ws.title = "Costos"

    columnas = ["ID", "Descripción", "Tipo de Costo"]
    ws.append(columnas)

    costos = Costo.objects.select_related("tipo_costo").all()

    for c in costos:
        ws.append([
            c.id,
            c.descripcion,
            c.tipo_costo.nombre if c.tipo_costo else "Sin tipo"
        ])

    response = HttpResponse(
        content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )
    response["Content-Disposition"] = 'attachment; filename="costos.xlsx"'

    wb.save(response)
    return response

def exportar_periodos_excel(request):
    wb = Workbook()
    ws = wb.active
    ws.title = "Periodos"

    columnas = ["ID", "Año", "Mes"]
    ws.append(columnas)

    periodos = Periodo.objects.all()

    for p in periodos:
        ws.append([
            p.id,
            getattr(p, "año", getattr(p, "anio", getattr(p, "ano", ""))),
            p.mes
        ])

    response = HttpResponse(
        content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )
    response["Content-Disposition"] = 'attachment; filename="periodos.xlsx"'

    wb.save(response)
    return response

@login_required
@rol_requerido('administrador')
def categoria(request):
    search = request.GET.get('search', '')
    categorias = TipoCosto.objects.all().order_by('id')  

    if search:
        categorias = categorias.filter(nombre__icontains=search)

    context = {
        'categorias': categorias,
        'search': search
    }
    return render(request, 'centro_costos/categoria.html', context)

@login_required
@rol_requerido('administrador')
def categoria_crear(request):
    if request.method == 'POST':
        form = TipoCostoForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Categoría creada exitosamente')
            return redirect('categoria')
        else:
            messages.error(request, 'Revisa los campos e intenta nuevamente')
    else:
        form = TipoCostoForm()

    return render(request, 'centro_costos/categoria_crear.html', {'form': form})

@login_required
@rol_requerido('administrador')
def categoria_act(request, pk):
    categoria = get_object_or_404(TipoCosto, pk=pk)

    if request.method == 'POST':
        form = TipoCostoForm(request.POST, instance=categoria)
        if form.is_valid():
            form.save()
            messages.success(request, 'Categoría actualizada exitosamente')
            return redirect('categoria')
        else:
            messages.error(request, 'Error al actualizar la categoría')
    else:
        form = TipoCostoForm(instance=categoria)

    return render(request, 'centro_costos/categoria_act.html', {'form': form, 'categoria': categoria})


@login_required
@rol_requerido('administrador')
def categoria_eliminar(request, pk):
    categoria = get_object_or_404(TipoCosto, pk=pk)

    if request.method == 'POST':
        categoria.delete()
        messages.success(request, 'Categoría eliminada exitosamente')
        return redirect('categoria')

    return render(request, 'centro_costos/categoria_eliminar.html', {'categoria': categoria})

@login_required
@rol_requerido('administrador')
def transaccion(request):
    transacciones = TransaccionCompra.objects.select_related('costo', 'costo__tipo_costo').all()
    
    item_costo_id = request.GET.get('item_costo')  
    if item_costo_id:
        transacciones = transacciones.filter(costo_id=item_costo_id)

    fecha_inicio = request.GET.get('fecha_inicio')
    fecha_fin = request.GET.get('fecha_fin')
    filtro_rapido = request.GET.get('filtro_rapido')

    if filtro_rapido == 'hoy':
        hoy = timezone.localdate()
        transacciones = transacciones.filter(created_at__date=hoy)
        fecha_inicio = None
        fecha_fin = None
    
    elif fecha_inicio and fecha_fin:
        try:
            fecha_inicio_dt = datetime.datetime.strptime(fecha_inicio, '%Y-%m-%d').date()
            fecha_fin_dt = datetime.datetime.strptime(fecha_fin, '%Y-%m-%d').date()
            
            transacciones = transacciones.filter(
                created_at__date__gte=fecha_inicio_dt,
                created_at__date__lte=fecha_fin_dt
            )
        except ValueError:
            messages.error(request, 'El formato de las fechas ingresadas no es válido.')

    context = {
        'transacciones': transacciones,
        'item_costos': Costo.objects.all(), 
        'selected_item_costo': item_costo_id,
        'selected_fecha_inicio': fecha_inicio,
        'selected_fecha_fin': fecha_fin,
        'selected_filtro_rapido': filtro_rapido,
    }

    return render(request, 'centro_costos/transaccion.html', context)



@login_required
@rol_requerido('administrador')
def transaccion_crear(request):
    if request.method == 'POST':
        form = TransaccionCompraForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Transacción creada exitosamente')
            return redirect('transaccion')
    else:
        form = TransaccionCompraForm()
    return render(request, 'centro_costos/transaccion_crear.html', {'form': form})


@login_required
@rol_requerido('administrador')
def transaccion_act(request, pk):
    transaccion = get_object_or_404(TransaccionCompra, pk=pk)
    if request.method == 'POST':
        form = TransaccionCompraForm(request.POST, instance=transaccion)
        if form.is_valid():
            form.save()
            messages.success(request, 'Transacción actualizada exitosamente')
            return redirect('transaccion')
    else:
        form = TransaccionCompraForm(instance=transaccion)
    return render(request, 'centro_costos/transaccion_act.html', {'form': form, 'transaccion': transaccion})


@login_required
@rol_requerido('administrador')
def transaccion_eliminar(request, pk):
    transaccion = get_object_or_404(TransaccionCompra, pk=pk)

    if request.method == 'POST':
        transaccion.delete()
        messages.success(request, "Transacción eliminada exitosamente")
        return redirect('transaccion')

    return render(request, 'centro_costos/transaccion_eliminar.html', {'transaccion': transaccion})
