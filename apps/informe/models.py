from django.db import models
from apps.paciente.models import Paciente
from apps.profesional_salud.models import ProfesionalSalud



class Informe(models.Model):
    paciente = models.ForeignKey(Paciente, on_delete=models.CASCADE)
    profesional_salud = models.ForeignKey(ProfesionalSalud, on_delete=models.CASCADE)
    titulo = models.CharField(max_length=200)
    fecha_informe=models.DateField()
    archivo = models.BinaryField(editable=True)
    llave_simetrica_encriptada = models.BinaryField()


class InformeTemporal(models.Model):
    paciente = models.ForeignKey(Paciente, on_delete=models.CASCADE)
    profesional_salud = models.ForeignKey(ProfesionalSalud, on_delete=models.CASCADE)
    titulo = models.CharField(max_length=200)
    fecha_informe=models.DateField()
    archivo = models.BinaryField(editable=True)
    llave_simetrica_encriptada = models.BinaryField()

