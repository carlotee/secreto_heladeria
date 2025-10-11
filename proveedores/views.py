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

def validar_rut(rut):
    rut_limpio = rut.replace(".", "").replace("-", "")
    
    if len(rut_limpio) < 2:
        return False
    
    rut_numero = rut_limpio[:-1]
    dv = rut_limpio[-1].upper()
    
    if not rut_numero.isdigit():
        return False
    
    suma = 0
    multiplo = 2
    
    for digito in reversed(rut_numero):
        suma += int(digito) * multiplo
        multiplo = 2 if multiplo == 7 else multiplo + 1
    
    dv_calculado = 11 - (suma % 11)
    
    if dv_calculado == 11:
        dv_calculado = '0'
    elif dv_calculado == 10:
        dv_calculado = 'K'
    else:
        dv_calculado = str(dv_calculado)
    
    return dv == dv_calculado


def validar_telefono(telefono):
    if not telefono:
        return True  
    
    tel_limpio = re.sub(r'[\s\-\(\)]', '', telefono)
    
    if not re.match(r'^\+?\d+$', tel_limpio):
        return False
    
    tel_numeros = tel_limpio.replace('+', '')
    
    return 8 <= len(tel_numeros) <= 15



def proveedor(request):
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


def proveedor_detalle(request, pk):
    proveedor = get_object_or_404(Proveedor, pk=pk, deleted_at__isnull=True)
    
    context = {
        'proveedor': proveedor
    }
    return render(request, 'proveedores/proveedor_detalle.html', context)

def validar_rut(rut):
    """Valida formato simple de RUT chileno: 12.345.678-9 o 12345678-9"""
    return bool(re.match(r'^\d{1,2}\.?\d{3}\.?\d{3}-[\dkK]$', rut))

def validar_telefono(telefono):
    """Valida formato chileno: +569XXXXXXXX o 9XXXXXXXX"""
    return bool(re.match(r'^(\+?56)?(\s?9\d{8})$', telefono))


# --- CREAR PROVEEDOR ---
def proveedor_crear(request):
    """Crea un nuevo proveedor según el modelo actual."""
    if request.method == 'POST':
        nombre = request.POST.get('nombre', '').strip()
        rut = request.POST.get('rut', '').strip()
        telefono = request.POST.get('telefono', '').strip()
        correo = request.POST.get('correo', '').strip()
        direccion = request.POST.get('direccion', '').strip()
        ciudad = request.POST.get('ciudad', '').strip()

        errores = []

        # ✅ Validar nombre (obligatorio)
        if not nombre:
            errores.append('El nombre es obligatorio.')

        # ✅ Validar RUT (obligatorio y único)
        if not rut:
            errores.append('El RUT es obligatorio.')
        elif not validar_rut(rut):
            errores.append('El formato del RUT no es válido (usa 12.345.678-9).')
        elif Proveedor.objects.filter(rut=rut).exists():
            errores.append('Ya existe un proveedor con ese RUT.')

        # ✅ Validar teléfono (solo si se ingresó)
        if telefono and not validar_telefono(telefono):
            errores.append('El formato del teléfono no es válido (usa +569XXXXXXXX).')

        # ✅ Validar correo (solo si se ingresó)
        if correo:
            try:
                validate_email(correo)
            except ValidationError:
                errores.append('El formato del correo no es válido.')

        # ✅ Mostrar errores si existen
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

        # ✅ Crear el proveedor
        Proveedor.objects.create(
            nombre=nombre,
            rut=rut,
            telefono=telefono if telefono else None,
            correo=correo,
            direccion=direccion,
            ciudad=ciudad
        )

        messages.success(request, f'Proveedor "{nombre}" creado exitosamente ✅')
        return redirect('proveedor')  # redirige al listado

    # Si es GET, renderiza formulario vacío
    return render(request, 'proveedores/proveedor_crear.html')



def proveedor_act(request, pk):
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
        
        if telefono and not validar_telefono(telefono):
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
        else:
            proveedor.nombre = nombre
            proveedor.rut = rut
            proveedor.telefono = telefono if telefono else None
            proveedor.correo = correo
            proveedor.direccion = direccion
            proveedor.ciudad = ciudad
            proveedor.save()
            messages.success(request, f'Proveedor "{nombre}" actualizado exitosamente')
            return redirect('proveedor')
    
    context = {
        'proveedor': proveedor,
        'is_edit': True
    }
    return render(request, 'proveedores/proveedor_act.html', context)


def proveedor_eliminar(request, pk):
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


def proveedor_restore(request, pk):
    proveedor = get_object_or_404(Proveedor, pk=pk)
    
    if request.method == 'POST':
        if proveedor.deleted_at:
            proveedor.deleted_at = None
            proveedor.save()
            messages.success(request, f'Proveedor "{proveedor.nombre}" restaurado exitosamente')
        else:
            messages.warning(request, 'El proveedor no estaba eliminado')
        return redirect('proveedor_list')
    
    context = {
        'proveedor': proveedor
    }
    return render(request, 'proveedores/proveedor_confirm_restore.html', context)


def proveedor_deleted_list(request):
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


def proveedor_permanent_delete(request, pk):
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

def proveedor_dashboard(request, proveedor_id):
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
    else:
        producto_form = ProductoForm()

    context = {
        'proveedor': proveedor,
        'productos': productos,
        'producto_form': producto_form,
    }
    return render(request, 'proveedores/prov_dashboard.html', context)