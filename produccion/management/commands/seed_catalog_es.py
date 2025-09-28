from django.core.management.base import BaseCommand
from produccion.models import Producto

class Command(BaseCommand):
    help = "Carga catálogo en español (productos)"

    def handle(self, *args, **kwargs):
        p1, _ = Producto.objects.get_or_create(
            nombre="Helado de Chocolate",
            defaults=dict(precio="500")
        )
        # ... crea p2..p5 similar ...
        self.stdout.write(self.style.SUCCESS("Catálogo cargado correctamente!"))