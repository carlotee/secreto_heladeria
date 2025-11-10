from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse, HttpResponseBadRequest
from django.views.decorators.http import require_POST
from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import Q
from .models import Producto, Proveedor
from .decorators import rol_requerido
from decimal import Decimal, InvalidOperation



@login_required
def producto(request):
    productos = Producto.objects.all().order_by('id')

    search = request.GET.get('search', '')
    if search:
        productos = productos.filter(
            Q(nombre__icontains=search) |
            Q(descripcion__icontains=search)
        )

    def parse_decimal(value):
        if not value or value in ('None', ''):
            return None
        try:
            return Decimal(str(value).replace(',', '.'))
        except (InvalidOperation, ValueError):
            return 'invalid'

    precio_min = parse_decimal(request.GET.get('precio_min'))
    precio_max = parse_decimal(request.GET.get('precio_max'))

    if precio_min not in (None, 'invalid'):
        productos = productos.filter(precio__gte=precio_min)
    if precio_max not in (None, 'invalid'):
        productos = productos.filter(precio__lte=precio_max)

    paginator = Paginator(productos, 5)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'productos': page_obj,
        'search': search,
        'precio_min': '' if precio_min in (None, 'invalid') else precio_min,
        'precio_max': '' if precio_max in (None, 'invalid') else precio_max,
        'total_productos': productos.count(),
        'precio_min_invalido': (precio_min == 'invalid'),
        'precio_max_invalido': (precio_max == 'invalid'),
    }
    return render(request, 'produccion/producto.html', context)

@login_required
def producto_detalle(request, pk):
    producto = get_object_or_404(Producto, pk=pk)
    
    context = {
        'producto': producto
    }
    return render(request, 'produccion/producto_detalle.html', context)


@login_required
@rol_requerido('proveedor', 'administrador')
def producto_crear(request):
    """Crea un producto y lo asocia a un proveedor."""
    if request.method == 'POST':
        nombre = request.POST.get('nombre', '').strip()
        descripcion = request.POST.get('descripcion', '').strip()
        precio = request.POST.get('precio', '').strip()
        stock = request.POST.get('stock', '').strip()
        proveedor_id = request.POST.get('proveedor', '').strip()

        errores = []

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
            stock = 0

        proveedor = None
        if proveedor_id:
            try:
                proveedor = Proveedor.objects.get(id=proveedor_id)
            except Proveedor.DoesNotExist:
                errores.append('El proveedor seleccionado no existe.')

        if errores:
            for error in errores:
                messages.error(request, error)
        else:
            Producto.objects.create(
                nombre=nombre,
                descripcion=descripcion,
                precio=precio,
                stock=stock,
                proveedor=proveedor
            )
            messages.success(request, f'Producto "{nombre}" creado exitosamente ✅')
            return redirect('producto')

    proveedores = Proveedor.objects.all()
    context = {'proveedores': proveedores}
    return render(request, 'produccion/producto_crear.html', context)


@login_required
@rol_requerido('proveedor', 'administrador')
def producto_act(request, pk):
    producto = get_object_or_404(Producto, pk=pk)
    
    if request.method == 'POST':
        nombre = request.POST.get('nombre')
        descripcion = request.POST.get('descripcion')
        precio = request.POST.get('precio')
        stock = request.POST.get('stock')
        
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
                    if stock:
                        producto.stock = int(stock)
                    producto.save()
                    messages.success(request, f'Producto "{nombre}" actualizado exitosamente ✅')
                    return redirect('producto')
            except ValueError:
                messages.error(request, 'El precio debe ser un número válido')
    
    context = {
        'producto': producto,
        'is_edit': True
    }
    return render(request, 'produccion/producto_act.html', context)


@login_required
@rol_requerido('administrador')
def producto_eliminar(request, pk):
    producto = get_object_or_404(Producto, pk=pk)
    
    if request.method == 'POST':
        nombre_producto = producto.nombre
        producto.delete()
        messages.success(request, f'Producto "{nombre_producto}" eliminado exitosamente.')
        return redirect('producto')
    
    context = {
        'producto': producto
    }
    return render(request, 'produccion/producto_eliminar.html', context)


@login_required
@rol_requerido('administrador')
@require_POST
def producto_delete_ajax(request, pk):
    """Elimina un producto y responde JSON para actualizar sin recargar."""
    if not request.headers.get("x-requested-with") == "XMLHttpRequest":
        return HttpResponseBadRequest("Solo AJAX")
    
    producto = get_object_or_404(Producto, pk=pk)
    nombre = producto.nombre
    producto.delete()

    return JsonResponse({"ok": True, "message": f"Producto '{nombre}' eliminado exitosamente"})


from django.http import HttpResponse
from openpyxl import Workbook
from .models import Producto

def exportar_productos_excel(request):
    wb = Workbook()
    ws = wb.active
    ws.title = "Productos"

    columnas = ["ID", "Nombre", "Descripción", "Precio", "Stock", "Proveedor"]
    ws.append(columnas)

    productos = Producto.objects.select_related("proveedor").all()
    for p in productos:
        ws.append([
            p.id,
            p.nombre,
            p.descripcion,
            float(p.precio),
            p.stock,
            p.proveedor.nombre if p.proveedor else "Sin proveedor"
        ])

    response = HttpResponse(
        content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )
    response["Content-Disposition"] = 'attachment; filename="productos.xlsx"'
    wb.save(response)
    return response
