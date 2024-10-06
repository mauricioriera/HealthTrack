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
class AceptarSolicitudForm(forms.Form):
    duracion_permiso = forms.IntegerField(label="Duración del permiso")
    llave = forms.CharField(
        widget=forms.Textarea(attrs={
            'placeholder': 'Ingrese su llave privada aquí...',
            'rows': 10,
            'cols': 40
        }),
    )
class DesencriptarArchivoForm(forms.Form):
    llave = forms.CharField(
        widget=forms.Textarea(attrs={
            'placeholder': 'Ingrese su llave privada aquí...',
            'rows':10,
            'cols':40
        }),
    )
