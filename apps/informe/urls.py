from django.urls import path
from apps.informe.views import (subir_archivo, mostrar_archivo_paciente, lista_archivos_paciente,
                                lista_archivos_profesional,mostrar_archivo_profesional)

urlpatterns = [
    path('subir_archivo/<int:profesional_id>/<int:paciente_id>', subir_archivo, name='subir_informe'),
    path('mostrar/<int:archivo_id>', mostrar_archivo_paciente, name='mostrar_archivo_paciente'),
    path('mostrar/profesional/<int:archivo_id>', mostrar_archivo_profesional, name='mostrar_archivo_profesional'),
    path('lista/paciente/<int:paciente_id>/', lista_archivos_paciente, name='lista_archivos_paciente'),
    path('lista/profesional/<int:paciente_id>/', lista_archivos_profesional, name='lista_archivos_profesional')
 ]