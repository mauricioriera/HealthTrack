from django import forms

from apps.informe.models import informe


class informeForm(forms.ModelForm):
    class Meta:
        model = informe
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
