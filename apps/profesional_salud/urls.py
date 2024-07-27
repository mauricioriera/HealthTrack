from django.urls import path
from apps.profesional_salud import views

urlpatterns =[

    path('prueba/', views.prueba, name='prueba'),
    path('principal/', views.vista_pincipal_ps, name='principal'),
    path('seleccion/', views.seleccion_paciente, name='seleccionar'),
    path('procesar/', views.procesar_paciente, name='procesar'),
    path('solicitar_acceso/<int:paciente_id>/', views.solicita_acceso, name='solicitar_acceso'),
    path('permitir_acceso/<int:user_id>/<int:paciente_id>', views.permitir_acceso, name='permitir_acceso'),
    path('denegar_acceso/<int:user_id>/<int:paciente_id>', views.eviar_mail_denegado, name='denegar_acceso'),
]
