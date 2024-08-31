from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from apps.profesional_salud.models import ProfesionalSalud


class ProfesionalSaludform(forms.ModelForm):
    class Meta:
        model = ProfesionalSalud
        fields = [
            'dni',
            'domicilio_consultorio',
            'especilidad',

        ]
        labels = {
            'dni': 'DNI',
            'domicilio_consultorio': 'dirección consultorio',
            'especilidad': 'espécialidad',

        }
        widgets = {
            'dni': forms.NumberInput(attrs={'class': 'form-control'}),
            'domicilio_consultorio': forms.TextImput(attrs={'class': 'form-control'}),
            'especilidad': forms.TextImput(attrs={'class': 'form-control'}),
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
