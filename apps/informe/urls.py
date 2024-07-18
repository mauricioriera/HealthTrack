from django.urls import path
from apps.informe.views import subir_archivo

urlpatterns = [
    path('subir_archivo/', subir_archivo, name='subir_archivo'),
 ]