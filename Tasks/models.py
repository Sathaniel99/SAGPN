from django.contrib.auth.models import AbstractUser
from django.utils.timezone import now
from django.db import models
from .choices import *

class Usuario(AbstractUser):
    rol = models.CharField(null=True,choices=Choices_Rol, default=Choices_Rol.TECNICO)
    img = models.ImageField(upload_to='usuarios/', null=True, blank=True)
    
    class Meta:
        verbose_name = "Usuario"
        verbose_name_plural = "Usuarios"
        
    def __str__(self):
        return f"{self.username} - {self.first_name}"


class Ticket(models.Model):
    # Relaciones con el modelo User (cliente y técnico)
    cliente = models.ForeignKey(Usuario, on_delete=models.CASCADE, null=True, blank=True, related_name='tickets_cliente')
    tecnico = models.ForeignKey(Usuario, on_delete=models.SET_NULL,limit_choices_to={'rol': 'Técnico'}, null=True, blank=True, related_name='tickets_tecnico')

    # Campos de texto
    situacion = models.CharField(max_length=20, default='')
    area = models.CharField(max_length=100, choices=Choices_Areas)  # areas donde se encuentra dicha situacion
    descripcion = models.TextField()  # detallada de la tarea

    # Fecha y hora
    fecha_ini = models.DateTimeField(default=now, null=True, blank=True)
    
    fecha_fin = models.DateTimeField(null=True, blank=True)  # Fecha de creación de la tarea

    # Prioridad
    prioridad = models.CharField(choices=Choices_Prioridades, default="------")

    # Estado de la tarea
    realizada = models.BooleanField(default=False)  # Indica si la tarea ha sido completada o no

    def __str__(self):
        return f"{self.id} - {self.situacion} - {self.area}"

    class Meta:
        verbose_name = "Ticket"
        verbose_name_plural = "Tickets"