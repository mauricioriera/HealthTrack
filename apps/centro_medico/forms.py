from django import forms

from apps.centro_medico.models import centro_medico


class centro_medicoForm(forms.ModelForm):
    class Meta:
        model = centro_medico
        fields = [
            'nombre_entidad',
            'domicilio',
            'telefono',
            'correo_electronico',
            'password',
        ]
