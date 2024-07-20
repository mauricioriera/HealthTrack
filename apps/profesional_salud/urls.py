from django.urls import path
from apps.profesional_salud import views

urlpatterns =[

    path('prueba/', views.prueba, name='prueba'),
    path('principal/', views.vista_pincipal_ps, name='principal'),
]
