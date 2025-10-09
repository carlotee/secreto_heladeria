from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.db.models import Q
from django.utils import timezone
from .models import Producto
from django.core.paginator import Paginator

def producto(request):
    productos = Producto.objects.filter(deleted_at__isnull=True).order_by('-created_at')
    
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
    
    paginator = Paginator(productos, 10)  
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'productos': page_obj,
        'search': search,
        'precio_min': precio_min,
        'precio_max': precio_max,
        'total_productos': productos.count()
    }
    return render(request, 'productos/producto.html', context)


def producto_detalle(request, pk):
    producto = get_object_or_404(Producto, pk=pk, deleted_at__isnull=True)
    
    context = {
        'producto': producto
    }
    return render(request, 'productos/producto_detalle.html', context)


def producto_crear(request):
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
                    Producto.objects.create(
                        nombre=nombre,
                        descripcion=descripcion,
                        precio=precio
                    )
                    messages.success(request, f'Producto "{nombre}" creado exitosamente')
                    return redirect('producto')
            except ValueError:
                messages.error(request, 'El precio debe ser un número válido')
    
    return render(request, 'productos/producto_crear.html')


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
    producto = get_object_or_404(Producto, pk=pk, deleted_at__isnull=True)
    
    if request.method == 'POST':
        producto.deleted_at = timezone.now()
        producto.save()
        messages.success(request, f'Producto "{producto.nombre}" eliminado exitosamente')
        return redirect('producto')
    
    context = {
        'producto': producto
    }
    return render(request, 'productos/producto_confirm_elim.html', context)
