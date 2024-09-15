from django.contrib.auth.models import User, Group
from Crypto.PublicKey import RSA
from django.db import models


class Paciente(models.Model):
    SEXO = (
        ('M', 'Masculino'),
        ('F', 'Femenino'),
    )
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    groups = models.ForeignKey(Group, null=True, blank=True, on_delete=models.CASCADE)
    fecha_nacimiento = models.DateField()
    dni = models.CharField(max_length=8)
    sexo = models.CharField(max_length=1, choices=SEXO, default='M')
    direccion = models.CharField(max_length=100)
    telefono = models.CharField(max_length=15)
    llave_publica = models.TextField(null=True)

    def __str__(self):
        return f"{self.user.first_name} {self.user.last_name}"

    def save(self, *args, **kwargs):
        if not self.llave_publica:
            key = RSA.generate(2048)
            self.llave_publica= key.public_key().export_key().decode('utf-8')
            self._llave_privada=key.export_key().decode('utf-8')
        super(Paciente, self).save(*args, **kwargs)

    def obtener_llave_privada(self):
        return self._llave_privada
