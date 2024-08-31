from django.contrib.auth.models import User, Group
from django.db import models


class ProfesionalSalud(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    groups = models.ForeignKey(Group, null=True, blank=True, on_delete=models.CASCADE)
    dni = models.IntegerField
    domicilio_consultorio = models.CharField(max_length=100)
    especilidad = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.user.first_name} {self.user.last_name}"