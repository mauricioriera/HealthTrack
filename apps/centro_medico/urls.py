from django.urls import path
from apps.centro_medico.views import centro_medico

urlpatterns =[
    path('centro_medico/',centro_medico),
]
