from django.db import models

from apps.paciente.models import paciente
from apps.profesional_salud.models import profesional_salud


class turno_profesional_salud(models.Model):
    paciente = models.OneToOneField(paciente, on_delete=models.CASCADE)
    profesional_salud = models.OneToOneField(profesional_salud, on_delete=models.CASCADE)
    fecha = models.DateField
    hora = models.DateTimeField
