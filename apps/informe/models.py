from django.db import models
from apps.paciente.models import Paciente
from apps.profesional_salud.models import ProfesionalSalud



class Informe(models.Model):
    paciente = models.ForeignKey(Paciente, on_delete=models.CASCADE)
    profesional_salud = models.ForeignKey(ProfesionalSalud, on_delete=models.CASCADE)
    titulo = models.CharField(max_length=200)
    fecha_informe=models.DateField()
    archivo = models.BinaryField(editable=True)
    llave_simetrica_encriptada = models.BinaryField()


class InformeTemporal(models.Model):
    paciente = models.ForeignKey(Paciente, on_delete=models.CASCADE)
    profesional_salud = models.ForeignKey(ProfesionalSalud, on_delete=models.CASCADE)
    titulo = models.CharField(max_length=200)
    fecha_informe=models.DateField()
    archivo = models.BinaryField(editable=True)
    llave_simetrica_encriptada = models.BinaryField()

class Solicitud(models.Model):
    ESTADO_CHOICES = [
        ('Pendiente', 'Pendiente'),
        ('Aceptada', 'Aceptada'),
        ('Rechazada', 'Rechazada'),
        ('Vencida','Vencida'),
    ]

    paciente = models.ForeignKey(Paciente, on_delete=models.CASCADE)
    profesional_salud = models.ForeignKey(ProfesionalSalud, on_delete=models.CASCADE)
    estado = models.CharField(max_length=10, choices=ESTADO_CHOICES, default='Pendiente')
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    tiempo_de_vida = models.IntegerField(null=True)

    def __str__(self):
        return f'Solicitud de {self.profesional_salud.username} a {self.paciente.username} - {self.estado}'