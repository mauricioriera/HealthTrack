from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from apps.paciente.models import paciente


class pacienteForm(forms.ModelForm):
    class Meta:
        model = paciente
        fields = [
            'fecha_nacimiento',
            'dni',
            'sexo',
            'domicilio',
            'telefono',
        ]
        labels = {
            'fecha_nacimiento': 'Fecha de Nacimiento',
            'dni': 'DNI',
            'sexo': 'Sexo',
            'domicilio': 'dirección',
            'telefono': 'Teléfono',
        }
        widgets = {

            'fecha_nacimiento': forms.DateField(attrs={'type': 'date'}),
            'dni': forms.NumberInput(attrs={'class': 'form-control'}),
            'sexo': forms.Select(attrs={'class': 'form-control'}),
            'domicilio': forms.TextImput(attrs={'class': 'form-control'}),
            'telfono': forms.NumberInput(attrs={'class': 'form-control'}),
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