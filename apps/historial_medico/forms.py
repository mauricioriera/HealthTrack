from django import forms

from apps.informe.models import informe


class informeForm(forms.ModelForm):
    class Meta:
        model = informe
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
