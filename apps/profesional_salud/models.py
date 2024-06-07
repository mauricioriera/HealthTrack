from django.db import models


class profesional_salud(models.Model):
    nombre = models.CharField(max_length=100)
    apellido = models.CharField(max_length=100)
    dni = models.IntegerField
    domicilio_consultorio = models.CharField(max_length=100)
    especilidad = models.CharField(max_length=100)
    correo_electronico = models.EmailField(max_length=100)
    password = models.CharField(max_length=20)
