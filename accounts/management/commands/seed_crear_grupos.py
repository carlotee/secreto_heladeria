from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group

class Command(BaseCommand):
    help = 'Crea los grupos de usuario necesarios'

    def handle(self, *args, **kwargs):
        grupos = ['Administrador', 'Proveedor', 'Cliente']
        
        for nombre_grupo in grupos:
            group, created = Group.objects.get_or_create(name=nombre_grupo)
            if created:
                self.stdout.write(self.style.SUCCESS(f'Grupo "{nombre_grupo}" creado'))
            else:
                self.stdout.write(self.style.WARNING(f'Grupo "{nombre_grupo}" ya existe'))