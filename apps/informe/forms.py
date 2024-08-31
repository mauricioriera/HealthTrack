from django import forms

from apps.informe.models import Informe


class InformeForm(forms.ModelForm):
    archivo = forms.FileField()
    titulo = forms.CharField()

    class Meta:
        model = Informe
        fields = [
            'titulo',
            'archivo',
            'fecha_informe',
        ]
        labels = {
            'titulo': 'Título del informe',
            'archivo': 'Informe',
            'fecha_informe': 'Fecha del informe',
        }
        widgets = {
            'fecha_informe': forms.DateInput(attrs={'type': 'date'}),
        }
class TiempoForm(forms.Form):
    duracion_permiso = forms.IntegerField(label="Duración del permiso")