from django.urls import path

from apps.centro_medico import views

urlpatterns =[
    path('centro_medico/',views.centro_medico, name='centro_medico',),
]
