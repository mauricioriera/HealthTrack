from django import forms
from django.contrib.auth.models import User

from apps.informe.models import informe
from apps.paciente.models import paciente
from apps.profesional_salud.models import profesional_salud


class informeForm(forms.ModelForm):
    paciente= forms.ModelChoiceField(queryset=paciente.objects.all())
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