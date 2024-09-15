from Crypto.PublicKey import RSA
from django.contrib.auth.models import User, Group
from django.db import models


class ProfesionalSalud(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    groups = models.ForeignKey(Group, null=True, blank=True, on_delete=models.CASCADE)
    matricula = models.CharField(max_length=12, null=True)
    domicilio_consultorio = models.CharField(max_length=100)
    especialidad = models.CharField(max_length=100)
    llave_publica=models.TextField(null=True)

    def __str__(self):
        return f"{self.user.first_name} {self.user.last_name}"

    def save(self, *args, **kwargs):
        if not self.llave_publica:
            key = RSA.generate(2048)
            self.llave_publica = key.public_key().export_key().decode('utf-8')
            self._llave_privada = key.export_key().decode('utf-8')
        super(ProfesionalSalud, self).save(*args, **kwargs)

    def obtener_llave_privada(self):
        return self._llave_privada