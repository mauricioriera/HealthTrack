from django import forms

from apps.historial_medico.models import historial_medico


class historial_medicoForm(forms.ModelForm):
    class Meta:
        model = historial_medico
        fields = [
            'paciente',
            'informe'
        ]
        labels = {
            'paciente': 'Paciente',
            'informe': 'informe',

        }
        widgets={
            'paciente': forms.Select(attrs={'class':'form-control'}),
            'informe': forms.Select(attrs={'class':'form-control'}),
        }
