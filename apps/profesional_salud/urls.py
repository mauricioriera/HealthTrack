from django.urls import path
from apps.profesional_salud import views

urlpatterns =[
    path('lista/', views.lista, name='lista'),
    path('prueba/', views.prueba, name='prueba')
]
