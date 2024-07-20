from django import forms
from django.contrib.auth.models import User

from apps.informe.models import informe
from apps.paciente.models import paciente
from apps.profesional_salud.models import profesional_salud


class informeForm(forms.ModelForm):
    paciente= forms.ModelChoiceField(queryset=paciente.objects.all())
    archivo= forms.FileField()
    class Meta:
        model = informe
        fields = [
            'paciente',
            'archivo',
        ]
        labels = {
            'paciente': 'Selecciona un paciente',
            'archivo': 'Cargar Informe',
        }