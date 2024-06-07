from django.db import models


class centro_medico(models.Model):
    nombre_entidad = models.CharField(max_length=100)
    domicilio = models.CharField(max_length=100)
    telefono = models.CharField(max_length=15)
    correo_electronico = models.EmailField(max_length=100)
    password = models.CharField(max_length=20)
