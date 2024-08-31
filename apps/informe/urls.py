from django.urls import path
from apps.informe.views import subir_archivo, mostrar_archivo, lista_archivos_paciente, lista_archivos_profesional

urlpatterns = [
    path('subir_archivo/<int:profesional_id>/<int:paciente_id>', subir_archivo, name='subir_informe'),
    path('mostrar/<int:archivo_id>/', mostrar_archivo, name='mostrar_archivo'),
    path('lista/paciente/<int:paciente_id>/', lista_archivos_paciente, name='lista_archivos_paciente'),
    path('lista/profesional/<str:token>/<str:tiempo_codificado>', lista_archivos_profesional, name='lista_archivos_profesional'),
 ]