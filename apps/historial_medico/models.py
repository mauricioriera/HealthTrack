from django.db import models

from apps.informe.models import informe
from apps.paciente.models import paciente


class historial_medico(models.Model):
    pociente = models.OneToOneField(paciente, null=True, blank=True, on_delete=models.CASCADE)
    informe = models.ForeignKey(informe, null=True, blank=True, on_delete=models.CASCADE)
