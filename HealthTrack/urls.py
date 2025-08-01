"""
URL configuration for HealthTrack project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
import django.contrib.auth
from django.contrib import admin
from django.urls import path, include
from HealthTrack.views import logout, inicio, CustomLoginView,custom_permission_denied_view,crear_usuario
from apps.informe import views


handler403 = custom_permission_denied_view

urlpatterns = [
    path('admin/', admin.site.urls, name='admin'),
    path('', inicio, name='inicio'),
    path('crear_usuario/', crear_usuario,name='crear_usuario'),
    path('accounts/login/', CustomLoginView.as_view(), name= 'login'),
    path('logout/', logout, name='logout'),
    path('profesional/',include('apps.profesional_salud.urls'), name='profesional'),
    path('informe/',include('apps.informe.urls'), name='informe'),
    path('paciente/',include('apps.paciente.urls'), name='paciente'),

]

views.start()

