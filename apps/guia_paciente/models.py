from django.db import models

from apps.paciente.models import paciente
from apps.turno_profesional_salud.models import turno_profesional_salud


class guia_paciente(models.Model):
    paciente = models.OneToOneField(paciente, null=True, blank=True, on_delete=models.CASCADE)
    turno_profesional_salud = models.ForeignKey(turno_profesional_salud, null=True, blank=True,
                                                on_delete=models.CASCADE)
