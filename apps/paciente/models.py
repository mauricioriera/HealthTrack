from django.contrib.auth.models import User, Group
from django.db import models


class paciente(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    groups = models.ForeignKey(Group, null=True, blank=True, on_delete=models.CASCADE)
    nombre = models.CharField(max_length=100)
    apellido = models.CharField(max_length=100)
    fecha_nacimiento = models.DateField
    dni = models.IntegerField
    sexo = models.CharField(max_length=50)
    domicilio = models.CharField(max_length=100)
    telefono = models.CharField(max_length=15)
    correo_electronico = models.EmailField(max_length=100)
    password = models.CharField(max_length=20)
