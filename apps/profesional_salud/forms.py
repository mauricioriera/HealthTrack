from django import forms

from apps.profesional_salud.models import profesional_salud


class profesional_saludForm(forms.ModelForm):
    class Meta:
        model = profesional_salud
        fields = [
            'nombre',
            'apellido',
            'dni',
            'domicilio_consultorio',
            'especilidad',
            'correo_electronico',
            'password',

        ]
        labels = {
            'nombre':'Nombre',
            'apellido':'Apellido',
            'dni':'DNI',
            'domicilio_consultorio':'dirección consultorio',
            'especilidad':'espécialidad',
            'correo_electronico':'email',
            'password':'contraseña',
        }
        widgets = {
            'nombre': forms.TextImput(attrs={'class':'form-control'}),
            'apellido':forms.TextImput(attrs={'class':'form-control'}),
            'dni':forms.NumberInput(attrs={'class':'form-control'}),
            'domicilio_consultorio':forms.TextImput(attrs={'class':'form-control'}),
            'especilidad':forms.TextImput(attrs={'class':'form-control'}),
            'correo_electronico':forms.EmailInput(attrs={'class':'form-control'}),
            'password':forms.PasswordInput(attrs={'class':'form-control'}),
        }
