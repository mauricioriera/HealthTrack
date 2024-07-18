from django.urls import path
from apps.paciente.views import PacienteCrear

urlpatterns =[
    path('crear/', PacienteCrear.as_view(), name='crear_paciente'),
    path('lista/', list, name='lista_paciente'),
]
