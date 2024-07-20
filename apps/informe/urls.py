from django.urls import path
from apps.informe.views import subir_archivo, mostrar_archivo, lista_archivos

urlpatterns = [
    path('subir_archivo/<int:profesional_id>/', subir_archivo, name='subir_informe'),
    path('mostrar/<int:archivo_id>/', mostrar_archivo, name='mostrar_archivo'),
    path('lista/<int:paciente_id>/', lista_archivos, name='lista_archivos'),
 ]