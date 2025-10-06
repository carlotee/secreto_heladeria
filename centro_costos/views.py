from django.shortcuts import render

# Create your views here.
def centro_costos_view(request):
    return render(request, 'centro_costos/centro_costos.html')

def costo(request, id):
    return render(request, 'centro_costos/costo.html', {'id': id})

def tipo_costo(request, tipo):
    return render(request, 'centro_costos/tipo_costo.html', {'tipo': tipo})
