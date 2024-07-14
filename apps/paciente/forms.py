from django import forms

from apps.paciente.models import paciente


class pacienteForm(forms.ModelForm):
    class Meta:
        model = paciente
        fields = [
            'nombre',
            'apellido',
            'fecha_nacimiento',
            'dni',
            'sexo',
            'domicilio',
            'telefono',
            'correo_electronico',
            'password',

        ]
        labels = {
            'nombre': 'Nombre',
            'apellido': 'Apellido',
            'fecha_nacimiento': 'Fecha de Nacimiento',
            'dni': 'DNI',
            'sexo': 'Sexo',
            'domicilio': 'dirección',
            'telefono': 'Teléfono',
            'correo_electronico': 'email',
            'password': 'contraseña',
        }
        widgets = {
            'nombre': forms.TextImput(attrs={'class': 'form-control'}),
            'apellido': forms.TextImput(attrs={'class': 'form-control'}),
            'fecha_nacimiento': forms.DateField(attrs={'type': 'date'}),
            'dni': forms.NumberInput(attrs={'class': 'form-control'}),
            'domicilio': forms.TextImput(attrs={'class': 'form-control'}),
            'telfono': forms.NumberInput(attrs={'class': 'form-control'}),
            'correo_electronico': forms.EmailInput(attrs={'class': 'form-control'}),
            'password': forms.PasswordInput(attrs={'class': 'form-control'}),
        }
