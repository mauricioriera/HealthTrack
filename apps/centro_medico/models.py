from django.contrib.auth.models import User, Group
from django.db import models


class centro_medico(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    groups = models.ForeignKey(Group, null=True, blank=True, on_delete=models.CASCADE)
    nombre_entidad = models.CharField(max_length=100)
    domicilio = models.CharField(max_length=100)
    telefono = models.CharField(max_length=15)
    correo_electronico = models.EmailField(max_length=100)
    password = models.CharField(max_length=20)
