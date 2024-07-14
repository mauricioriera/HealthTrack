from django.urls import path
from apps.informe import views

urlpatterns =[
    path('crear_informe/',views.InformeCrear.as_view(), name='crear_informe',),
]