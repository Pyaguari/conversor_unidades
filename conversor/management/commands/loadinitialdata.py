from django.core.management.base import BaseCommand
from django.core.management import call_command

class Command(BaseCommand):
    help = 'Carga datos iniciales'

    def handle(self, *args, **options):
        self.stdout.write('Cargando datos iniciales...')
        call_command('loaddata', 'initial_data.json')
        self.stdout.write(self.style.SUCCESS('Datos cargados exitosamente'))