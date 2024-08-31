from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


from apps.paciente.models import Paciente


class Pacienteform(forms.ModelForm):
    class Meta:
        model = Paciente
        fields = [
            'fecha_nacimiento',
            'dni',
            'sexo',
            'direccion',
            'telefono',
        ]
        labels = {
            'fecha_nacimiento': 'Fecha de Nacimiento',
            'dni': 'DNI',
            'sexo': 'Sexo',
            'direccion': 'Dirección',
            'telefono': 'Teléfono',
        }
        widgets = {

            'fecha_nacimiento': forms.DateInput(attrs={'type':'date'}),
            'dni': forms.TextInput(attrs={'class': 'form-control'}),
            'sexo': forms.Select(attrs={'class': 'form-control'}),
            'direccion': forms.TextInput(attrs={'class': 'form-control'}),
            'telefono': forms.NumberInput(attrs={'class': 'form-control'}),
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