from django.contrib.auth.models import User, Group
from django.db import models


class paciente(models.Model):
    SEXO = (
        ('M', 'masculino'),
        ('F', 'femenino'),
    )
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    groups = models.ForeignKey(Group, null=True, blank=True, on_delete=models.CASCADE)
    fecha_nacimiento = models.DateField()
    dni = models.CharField(max_length=8)
    sexo = models.CharField(max_length=1, choices=SEXO, default='M')
    direccion = models.CharField(max_length=100)
    telefono = models.CharField(max_length=15)
