from django.urls import path
from apps.profesional_salud import views
from apps.profesional_salud.views import principal

urlpatterns =[
    path('principal/', principal.as_view(), name='principal'),
    path('solicitar_acceso/<int:paciente_id>/', views.solicita_acceso, name='solicitar_acceso'),
    path('permitir_acceso/<int:user_id>/<int:paciente_id>', views.solicitar_tiempo_acceso, name='permitir_acceso'),
    path('denegar_acceso/<int:user_id>/<int:paciente_id>', views.eviar_mail_denegado, name='denegar_acceso'),
]
