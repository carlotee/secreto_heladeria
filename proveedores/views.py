from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.db.models import Q
from django.utils import timezone
from django.core.exceptions import ValidationError
from django.core.validators import validate_email
from .models import Proveedor
from django.core.paginator import Paginator
from .forms import ProveedorForm
import re
from produccion.models import Producto
from produccion.forms import ProductoForm
from common.decorators_prov import rol_requerido_proveedor 
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from openpyxl import Workbook
from common.decorators_pe import rol_requerido_pe



def validar_rut(rut):
    """Valida formato simple de RUT chileno: 12.345.678-9 o 12345678-9"""
    return bool(re.match(r'^\d{1,2}\.?\d{3}\.?\d{3}-[\dkK]$', rut))

def validar_telefono(telefono):
    """Valida formato chileno: +569XXXXXXXX (debe incluir +)"""
    return bool(re.match(r'^\+569\d{8}$', telefono))



@login_required 
@rol_requerido_pe('administrador')
def proveedor(request):
    """Muestra el listado paginado de proveedores activos."""
    proveedores = Proveedor.objects.filter(deleted_at__isnull=True).order_by('nombre')
    
    search = request.GET.get('search', '')
    if search:
        proveedores = proveedores.filter(
            Q(nombre__icontains=search) |
            Q(rut__icontains=search) |
            Q(correo__icontains=search) |
            Q(ciudad__icontains=search)
        )
    
    ciudad = request.GET.get('ciudad')
    if ciudad:
        proveedores = proveedores.filter(ciudad__iexact=ciudad)
    
    ciudades = Proveedor.objects.filter(
        deleted_at__isnull=True
    ).values_list('ciudad', flat=True).distinct().order_by('ciudad')
    
    paginator = Paginator(proveedores, 15) 	
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'proveedores': page_obj,
        'search': search,
        'ciudades': ciudades,
        'ciudad_seleccionada': ciudad,
        'total_proveedores': proveedores.count()
    }
    return render(request, 'proveedores/proveedor.html', context)


@login_required 
def proveedor_detalle(request, pk):
    """Muestra el detalle de un proveedor y sus productos asociados."""
    proveedor = get_object_or_404(Proveedor, pk=pk)
    productos = proveedor.productos.all() 	

    context = {
        'proveedor': proveedor,
        'productos': productos, 
    }
    return render(request, 'proveedores/proveedor_detalle.html', context)



@login_required
@rol_requerido_proveedor('proveedor', 'administrador')
def proveedor_crear(request):
    """Crea un nuevo proveedor."""
    if request.method == 'POST':
        nombre = request.POST.get('nombre', '').strip()
        rut = request.POST.get('rut', '').strip()
        telefono = request.POST.get('telefono', '').strip()
        correo = request.POST.get('correo', '').strip()
        direccion = request.POST.get('direccion', '').strip()
        ciudad = request.POST.get('ciudad', '').strip()

        errores = []

        if not nombre:
            errores.append('El nombre es obligatorio.')
        elif len(nombre) > 50:
            errores.append('El nombre no puede exceder los 50 caracteres.')

        if not rut:
            errores.append('El RUT es obligatorio.')
        elif not validar_rut(rut):
            errores.append('El formato del RUT no es válido (usa 12.345.678-9).')
        elif Proveedor.objects.filter(rut=rut, deleted_at__isnull=True).exists():
            errores.append('Ya existe un proveedor activo con ese RUT.')

        if telefono:
            if not telefono.startswith('+'):
                errores.append('El teléfono debe comenzar con el símbolo +')
            elif not validar_telefono(telefono):
                 errores.append('El formato del teléfono no es válido (usa +569XXXXXXXX).')

        if correo:
            try:
                validate_email(correo)
            except ValidationError:
                errores.append('El formato del correo no es válido.')

        if ciudad and len(ciudad) > 30:
            errores.append('La ciudad no puede exceder los 30 caracteres.')

        if errores:
            for error in errores:
                messages.error(request, error)

            context = {
                'nombre': nombre,
                'rut': rut,
                'telefono': telefono,
                'correo': correo,
                'direccion': direccion,
                'ciudad': ciudad,
            }
            return render(request, 'proveedores/proveedor_crear.html', context)

        Proveedor.objects.create(
            nombre=nombre,
            rut=rut,
            telefono=telefono if telefono else None,
            correo=correo,
            direccion=direccion,
            ciudad=ciudad
        )

        messages.success(request, f'Proveedor "{nombre}" creado exitosamente ✅')

        context = {}
        return render(request, 'proveedores/proveedor_crear.html', context)

    return render(request, 'proveedores/proveedor_crear.html')


@login_required 
@rol_requerido_proveedor('proveedor', 'administrador')
def proveedor_act(request, pk):
    """Actualiza un proveedor existente."""
    proveedor = get_object_or_404(Proveedor, pk=pk, deleted_at__isnull=True)
    
    if request.method == 'POST':
        nombre = request.POST.get('nombre', '').strip()
        rut = request.POST.get('rut', '').strip()
        telefono = request.POST.get('telefono', '').strip()
        correo = request.POST.get('correo', '').strip()
        direccion = request.POST.get('direccion', '').strip()
        ciudad = request.POST.get('ciudad', '').strip()
        
        errores = []
        
        if not nombre:
            errores.append('El nombre es obligatorio')
        
        if not rut:
            errores.append('El RUT es obligatorio')
        elif not validar_rut(rut):
            errores.append('El RUT ingresado no es válido')
        elif Proveedor.objects.filter(rut=rut, deleted_at__isnull=True).exclude(pk=proveedor.pk).exists():
            errores.append('Ya existe otro proveedor activo con ese RUT.')
        
        if telefono:
            if not telefono.startswith('+'):
                errores.append('El teléfono debe comenzar con el símbolo +')
            elif not validar_telefono(telefono):
                errores.append('El formato del teléfono no es válido')
        
        if not correo:
            errores.append('El correo es obligatorio')
        else:
            try:
                validate_email(correo)
            except ValidationError:
                errores.append('El formato del correo no es válido')
                
        if not direccion:
            errores.append('La dirección es obligatoria')
        if not ciudad:
            errores.append('La ciudad es obligatoria')
        
        
        if errores:
            for error in errores:
                messages.error(request, error)
            
            context = {
                'proveedor': proveedor,
                'form_data': {
                    'nombre': nombre,
                    'rut': rut,
                    'telefono': telefono,
                    'correo': correo,
                    'direccion': direccion,
                    'ciudad': ciudad,
                },
                'is_edit': True
            }
            return render(request, 'proveedores/proveedor_act.html', context)
        
        
        proveedor.nombre = nombre
        proveedor.rut = rut
        proveedor.telefono = telefono if telefono else None
        proveedor.correo = correo
        proveedor.direccion = direccion
        proveedor.ciudad = ciudad
        proveedor.save()
        
        messages.success(request, f'Proveedor "{nombre}" actualizado exitosamente.')

        return redirect('proveedor')
    
    context = {
        'proveedor': proveedor,
        'is_edit': True
    }
    return render(request, 'proveedores/proveedor_act.html', context)


@login_required
@rol_requerido_proveedor('administrador')
def proveedor_eliminar(request, pk):
    """Realiza la eliminación lógica (soft-delete) de un proveedor."""
    proveedor = get_object_or_404(Proveedor, pk=pk, deleted_at__isnull=True)
    
    if request.method == 'POST':
        proveedor.deleted_at = timezone.now()
        proveedor.save()
        messages.success(request, f'Proveedor "{proveedor.nombre}" eliminado exitosamente')
        return redirect('proveedor')
    
    context = {
        'proveedor': proveedor
    }
    return render(request, 'proveedores/proveedor_confirm_elim.html', context)


@login_required
@rol_requerido_proveedor('administrador')
def proveedor_restore(request, pk):
    """Restaura (quita soft-delete) un proveedor."""
    proveedor = get_object_or_404(Proveedor, pk=pk)
    
    if request.method == 'POST':
        if proveedor.deleted_at:
            proveedor.deleted_at = None
            proveedor.save()
            messages.success(request, f'Proveedor "{proveedor.nombre}" restaurado exitosamente')
        else:
            messages.warning(request, 'El proveedor no estaba eliminado')
        return redirect('proveedor_deleted_list') 
    
    context = {
        'proveedor': proveedor
    }
    return render(request, 'proveedores/proveedor_confirm_restore.html', context)


@login_required 
@rol_requerido_proveedor('administrador')
def proveedor_deleted_list(request):
    """Muestra la lista de proveedores eliminados (soft-deleted)."""
    proveedores = Proveedor.objects.filter(deleted_at__isnull=False).order_by('-deleted_at')
    
    search = request.GET.get('search', '')
    if search:
        proveedores = proveedores.filter(
            Q(nombre__icontains=search) |
            Q(rut__icontains=search) |
            Q(correo__icontains=search)
        )
    
    context = {
        'proveedores': proveedores,
        'search': search
    }
    return render(request, 'proveedores/proveedor_deleted_list.html', context)


@login_required 
@rol_requerido_proveedor('administrador')
def proveedor_permanent_delete(request, pk):
    """Elimina permanentemente un proveedor de la base de datos."""
    proveedor = get_object_or_404(Proveedor, pk=pk)
    
    if request.method == 'POST':
        nombre = proveedor.nombre
        proveedor.delete() 
        messages.success(request, f'Proveedor "{nombre}" eliminado permanentemente')
        return redirect('proveedor_deleted_list')
    
    context = {
        'proveedor': proveedor
    }
    return render(request, 'proveedores/proveedor_confirm_permanent_delete.html', context)


@login_required 
@rol_requerido_proveedor('proveedor', 'administrador')
def proveedor_dashboard(request, proveedor_id):
    """Dashboard para la gestión de productos de un proveedor."""
    proveedor = get_object_or_404(Proveedor, pk=proveedor_id, deleted_at__isnull=True)
    productos = Producto.objects.filter(proveedor=proveedor).order_by('nombre')

    if request.method == 'POST':
        producto_form = ProductoForm(request.POST)
        if producto_form.is_valid():
            producto = producto_form.save(commit=False)
            producto.proveedor = proveedor
            producto.save()
            messages.success(request, f'✅ Producto "{producto.nombre}" agregado correctamente.')
            return redirect('proveedor_dashboard', proveedor_id=proveedor.id)
        
        messages.error(request, 'Error al agregar producto. Revisa los campos.')
    else:
        producto_form = ProductoForm()

    context = {
        'proveedor': proveedor,
        'productos': productos,
        'producto_form': producto_form,
    }
    return render(request, 'proveedores/prov_dashboard.html', context)


@rol_requerido_proveedor('administrador') 
def exportar_proveedores_excel(request):
    """Exporta la lista completa de proveedores a un archivo Excel."""
    wb = Workbook()
    ws = wb.active
    ws.title = "Proveedores"

    columnas = ["ID", "Nombre", "RUT", "Teléfono", "Correo", "Dirección", "Ciudad"]
    ws.append(columnas)

    proveedores = Proveedor.objects.all()

    for p in proveedores:
        ws.append([
            p.id,
            p.nombre,
            p.rut if hasattr(p, "rut") else "",
            p.telefono if hasattr(p, "telefono") else "",
            p.correo if hasattr(p, "correo") else "",
            p.direccion if hasattr(p, "direccion") else "",
            p.ciudad if hasattr(p, "ciudad") else "",
        ])

    response = HttpResponse(
        content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )
    response["Content-Disposition"] = 'attachment; filename="proveedores.xlsx"'
    wb.save(response)
    return response