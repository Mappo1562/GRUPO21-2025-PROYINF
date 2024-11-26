from django.contrib.auth.models import User
from django.db import models

class Profile(models.Model):
    ROLE_CHOICES = [
        ('O','Operador'),
        ('A','Administrador'),
        ('B','Bibliotecóloga'),
    ]
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES)


class Solicitud(models.Model):
    title = models.CharField(max_length=255)
    content = models.TextField()
    aprobado = models.BooleanField(default=False) 
    created_at = models.DateTimeField(auto_now_add=True)
#coimentario pruebva

class Preenvios(models.Model):
    title = models.CharField(max_length=255)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

