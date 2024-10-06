from django.urls import path

from apps.paciente import views
from apps.paciente.views import PacienteCrear

urlpatterns =[
    path('crear/', PacienteCrear.as_view(), name='crear_paciente'),
    path('aceptar_solicitud/<int:medico_id>/<int:paciente_id>', views.aceptar_solicitud, name='aceptar_solitud'),
]
