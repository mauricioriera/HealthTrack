from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from apps.profesional_salud.models import ProfesionalSalud


class ProfesionalSaludform(forms.ModelForm):
    class Meta:
        model = ProfesionalSalud
        fields = [
            'matricula',
            'domicilio_consultorio',
            'especialidad',

        ]
        labels = {
            'matricula': 'Matricula número',
            'domicilio_consultorio': 'Dirección Consultorio',
            'especialidad': 'Especialidad',

        }
        widgets = {
            'matricula': forms.TextInput(attrs={'class': 'form-control'}),
            'domicilio_consultorio': forms.TextInput(attrs={'class': 'form-control'}),
            'especialidad': forms.TextInput(attrs={'class': 'form-control'}),
        }


class RegistroForm(UserCreationForm):
    class Meta:
        model = User

        fields = [
            'username',
            'first_name',
            'last_name',
            'email',
        ]
        labels = {
            'username': 'Usuario:',
            'first_name': 'Nombre:',
            'last_name': 'Apellido:',
            'email': 'Correo:',
        }
