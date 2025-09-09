from django.db import models

class Usuarios(models.Model):
    id_usuario = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=45)
    apellidop = models.CharField(max_length=45)
    apellidom = models.CharField(max_length=45)
    telefono = models.CharField(max_length=45)
    correo = models.EmailField(max_length=45)
    contrasenia = models.TextField()

    class Meta:
        db_table = 'usuarios'