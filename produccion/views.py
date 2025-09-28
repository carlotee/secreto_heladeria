from django.shortcuts import render
from .models import Producto
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect
from produccion.forms import ProductoForm

# Create your views here.
@login_required
def producto_lista(request):
    productos = Producto.objects.all()

    return render(request, "produccion/producto.html", {
        "productos": productos,
    })

@login_required
def detalle_compra(request, pk):
    producto = get_object_or_404(Producto, pk=pk)
    valor_unitario = Producto.objects.filter(producto=producto).order_by('-date')[:10]
    cantidad_total = Producto.objects.filter(producto=producto).order_by('-date')[:10]
    estado = Producto.objects.filter(producto=producto).order_by('-date')[:10]

    return render(request, 'produccion/detalle_compra.html', {
        'producto': producto,
        'valor_unitario': valor_unitario,
        'cantidad_total': cantidad_total,
        'estado': estado,
    })


@login_required
def crear_producto(request):
    if request.method == 'POST':
        form = ProductoForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('producto_lista')
    else:
        form = ProductoForm()
    return render(request, 'produccion/crear_producto.html', {'form': form})
