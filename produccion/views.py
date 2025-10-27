from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.db.models import Q
from django.utils import timezone
from .models import Producto
from django.core.paginator import Paginator
from proveedores.models import Proveedor

def producto(request):
    productos = Producto.objects.all().order_by('id')
    
    search = request.GET.get('search', '')
    if search:
        productos = productos.filter(
            Q(nombre__icontains=search) | 
            Q(descripcion__icontains=search)
        )
    
    precio_min = request.GET.get('precio_min')
    precio_max = request.GET.get('precio_max')
    
    if precio_min:
        productos = productos.filter(precio__gte=precio_min)
    if precio_max:
        productos = productos.filter(precio__lte=precio_max)
    
    paginator = Paginator(productos, 5)  
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'productos': page_obj,
        'search': search,
        'precio_min': precio_min,
        'precio_max': precio_max,
        'total_productos': productos.count()
    }
    return render(request, 'produccion/producto.html', context)


def producto_detalle(request, pk):
    producto = get_object_or_404(Producto, pk=pk)
    
    context = {
        'producto': producto
    }
    return render(request, 'produccion/producto_detalle.html', context)

def producto_crear(request):
    """Crea un producto y lo asocia a un proveedor."""
    if request.method == 'POST':
        nombre = request.POST.get('nombre', '').strip()
        descripcion = request.POST.get('descripcion', '').strip()
        precio = request.POST.get('precio', '').strip()
        stock = request.POST.get('stock', '').strip()
        proveedor_id = request.POST.get('proveedor', '').strip()

        errores = []

        # 🔹 Validaciones básicas
        if not nombre:
            errores.append('El nombre del producto es obligatorio.')
        if not precio:
            errores.append('El precio del producto es obligatorio.')
        else:
            try:
                precio = float(precio)
                if precio < 0:
                    errores.append('El precio no puede ser negativo.')
            except ValueError:
                errores.append('El precio debe ser un número válido.')

        if stock:
            try:
                stock = int(stock)
                if stock < 0:
                    errores.append('El stock no puede ser negativo.')
            except ValueError:
                errores.append('El stock debe ser un número entero.')
        else:
            stock = 0  # valor por defecto

        # 🔹 Proveedor
        proveedor = None
        if proveedor_id:
            try:
                proveedor = Proveedor.objects.get(id=proveedor_id)
            except Proveedor.DoesNotExist:
                errores.append('El proveedor seleccionado no existe.')

        # 🔹 Mostrar errores si hay
        if errores:
            for error in errores:
                messages.error(request, error)
        else:
            # 🔹 Crear producto
            Producto.objects.create(
                nombre=nombre,
                descripcion=descripcion,
                precio=precio,
                stock=stock,
                proveedor=proveedor
            )
            messages.success(request, f'Producto "{nombre}" creado exitosamente ✅')
            return redirect('producto')

    # 🔹 Pasar lista de proveedores al template
    proveedores = Proveedor.objects.all()
    context = {'proveedores': proveedores}
    return render(request, 'produccion/producto_crear.html', context)


def producto_act(request, pk):
    producto = get_object_or_404(Producto, pk=pk, deleted_at__isnull=True)
    
    if request.method == 'POST':
        nombre = request.POST.get('nombre')
        descripcion = request.POST.get('descripcion')
        precio = request.POST.get('precio')
        
        if not nombre:
            messages.error(request, 'El nombre del producto es obligatorio')
        elif not precio:
            messages.error(request, 'El precio del producto es obligatorio')
        else:
            try:
                precio = float(precio)
                if precio < 0:
                    messages.error(request, 'El precio no puede ser negativo')
                else:
                    producto.nombre = nombre
                    producto.descripcion = descripcion
                    producto.precio = precio
                    producto.save()
                    messages.success(request, f'Producto "{nombre}" actualizado exitosamente')
                    return redirect('producto')
            except ValueError:
                messages.error(request, 'El precio debe ser un número válido')
    
    context = {
        'producto': producto,
        'is_edit': True
    }
    return render(request, 'productos/producto_act.html', context)


def producto_eliminar(request, pk):
    producto = get_object_or_404(Producto, pk=pk)
    
    if request.method == 'POST':
        nombre_producto = producto.nombre  # guardamos el nombre para mostrarlo después
        producto.delete()  # elimina realmente de la base de datos
        messages.success(request, f'Producto "{nombre_producto}" eliminado exitosamente.')
        return redirect('producto')  # asegúrate que 'producto' sea el nombre de la URL del listado
    
    context = {
        'producto': producto
    }
    return render(request, 'produccion/producto_eliminar.html', context)

from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse, HttpResponseBadRequest
from django.views.decorators.http import require_POST


@require_POST
def producto_delete_ajax(request, pk):
    if not request.headers.get("x-requested-with") == "XMLHttpRequest":
        return HttpResponseBadRequest("Solo AJAX")
    producto = get_object_or_404(Producto, pk=pk)
    nombre = producto.nombre
    producto.delete()

    return JsonResponse({"ok": True, "message": f"Producto '{nombre}' eliminada"})