from django.contrib.auth.models import AbstractUser
from django.db import models

class Usuario(AbstractUser):
    ROLES = (
        ('admin', 'Administrador'),
        ('usuario', 'Usuario'),
    )
    rol = models.CharField(max_length=10, choices=ROLES, default='usuario')

    # Campo para la edad
    edad = models.IntegerField(null=True, blank=True)
    
    # Otros campos que puedas querer agregar, por ejemplo:
    direccion = models.CharField(max_length=255, null=True, blank=True)
    telefono = models.CharField(max_length=20, null=True, blank=True)
    
    # Métodos adicionales que puedan ser necesarios
    def __str__(self):
        return self.username  # Esto devuelve el nombre de usuario como representación del objeto

    # Opcional: Si deseas agregar validaciones adicionales o personalizaciones
    def save(self, *args, **kwargs):
        # Lógica personalizada de guardado, si es necesario
        super().save(*args, **kwargs)


#------------------------------------------
#
#               Contacto
#
#------------------------------------------
class MensajeContacto(models.Model):
    nombre = models.CharField(max_length=100)
    email = models.EmailField()
    mensaje = models.TextField()
    fecha = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Mensaje de {self.nombre} - {self.email}"