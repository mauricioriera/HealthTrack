from django import forms
from django.contrib.auth.models import User

from apps.informe.models import informe
from apps.paciente.models import paciente
from apps.profesional_salud.models import profesional_salud


class informeForm(forms.ModelForm):
    paciente= forms.ModelChoiceField(queryset=paciente.objects.all())
    profesional: forms.ModelChoiceField(queryset=profesional_salud.objects.all())
    archivo: forms.FileField()
    class Meta:
        model = informe
        fields = [
            'paciente',
            'profesional_salud',
            'archivo',
        ]
        labels = {
            'paciente': 'Selecciona un paciente',
            'profesional_salud': 'Medico',
            'archivo': 'Cargar Informe',
        }

