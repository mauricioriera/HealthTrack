from django import forms
from apps.informe.models import informe
from apps.paciente.models import paciente


class informeForm(forms.ModelForm):
    paciente= forms.ModelChoiceField(queryset=paciente.objects.filter(groups=1))
    archivo= forms.FileField()
    titulo= forms.CharField()
    class Meta:
        model = informe
        fields = [
            'paciente',
            'titulo',
            'archivo',
        ]
        labels = {
            'paciente':'Paciente',
            'titulo':'Título del informe',
            'archivo':'Informe',
        }