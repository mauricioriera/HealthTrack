from django.apps import AppConfig


class InformeConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.informe'

    def ready(self):
        print('ready...')
