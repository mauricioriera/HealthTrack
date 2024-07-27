from django.urls import path
from apps.profesional_salud import views

urlpatterns =[

    path('prueba/', views.prueba, name='prueba'),
    path('principal/', views.vista_pincipal_ps, name='principal'),
    path('seleccion/', views.seleccion_paciente, name='seleccionar'),
    path('procesar/', views.procesar_paciente, name='procesar'),
    path('solicitar_acceso/<int:paciente_id>/', views.solicita_acceso, name='solicitar_acceso'),
    path('acceso/<str:token>/', views.verificar_magic_link, name='verificar_magic_link'),
    path('permitir_acceso/<int:user_id>/<int:paciente_id>', views.permitir_acceso, name='permitir_acceso')
]
