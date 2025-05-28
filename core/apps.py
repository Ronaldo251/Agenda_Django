# core/apps.py

from django.apps import AppConfig

class CoreConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'core'

    def ready(self):
        from django.db.utils import OperationalError
        from core.models import Categoria
        try:
            categorias = [
                ('aniversario', '#f39c12'),
                ('festa', '#e74c3c'),
                ('reuniao', '#3498db'),
                ('trabalho', '#2ecc71'),
            ]
            for nome, cor in categorias:
                Categoria.objects.get_or_create(nome=nome, defaults={'cor': cor})
        except OperationalError:
            # Evita erro durante as migrações iniciais, pois a tabela pode não existir ainda
            pass
