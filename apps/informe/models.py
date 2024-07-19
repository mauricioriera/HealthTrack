from django.db import models

from apps.paciente.models import paciente
from apps.profesional_salud.models import profesional_salud


class informe(models.Model):
    paciente = models.ForeignKey(paciente, on_delete=models.CASCADE)
    profesional_salud = models.ForeignKey(profesional_salud, on_delete=models.CASCADE)
    archivo = models.BinaryField(editable=True)
