from django.db import models

from apps.centro_medico.models import centro_medico
from apps.paciente.models import paciente


class turno_centro_medico(models.Model):
    paciente = models.OneToOneField(paciente, on_delete=models.CASCADE)
    centro_medico = models.ForeignKey(centro_medico, on_delete=models.CASCADE)
    fecha = models.DateField
    hora = models.DateTimeField
