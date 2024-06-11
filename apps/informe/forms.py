from django import forms

from apps.historial_medico.models import historial_medico


class historial_medicoForm(forms.ModelForm):
    class Meta:
        model = historial_medico
        fields = [
            'paciente',
            'profesional_salud',
            'archivo',
        ]
        labels = {
            'paciente': 'Paciente',
            'profesional_salud': 'Medico',
            'archivo': 'Cargar Informe',
        }
        widgets={
            'paciente': forms.Select,
            'profesional_salud': forms.Select(attrs={'class':'form-control'}),
            'archivo': forms.FileField(required=True),
        }
