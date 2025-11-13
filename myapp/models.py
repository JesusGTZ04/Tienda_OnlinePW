from django.db import models
from decimal import Decimal
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    email = models.EmailField( max_length=255, unique=True)
    telefono = models.CharField(max_length=15)
    direccion = models.CharField(max_length=255)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    def __str__(self):
        return self.email
    
    class meta:
        verbose_name = "Cliente"
        verbose_name_plural = "Clientes"


class Categoria(models.Model):
    nombre_categoria = models.CharField(max_length=45)
    def __str__(self):
        return self.nombre_categoria
    
class Subcategoria(models.Model):
    nombre_subcategoria = models.CharField(max_length=45)
    categoria = models.ForeignKey(Categoria, on_delete=models.CASCADE)
    def __str__(self):
        return f"{self.nombre_subcategoria}"
    
class Producto(models.Model):
    nombre_producto = models.CharField(max_length=50)
    precio = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.IntegerField(default=0)
    genero = models.CharField(max_length=45)
    subcategoria = models.ForeignKey(Subcategoria, on_delete=models.CASCADE)
    descripcion = models.TextField(default="")
    def __str__(self):
        return self.nombre_producto
    
class ImagenProducto(models.Model):
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    imagen = models.ImageField( upload_to='productos_img/', max_length=300)
    principal = models.BooleanField(default=False)
    fecha_subida = models.DateField(auto_now_add=True)
    def __str__(self):
        return f"Imagen de {self.producto.nombre_producto}"
    
class Venta(models.Model):
    fecha_venta = models.DateField(auto_now_add=True)
    total = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal(0.00))
    cliente = models.ForeignKey(User, on_delete=models.PROTECT)
    def __str__(self):
        return f"Venta {self.id} de {self.cliente.email}"

class DetalleVenta(models.Model):
    venta = models.ForeignKey(Venta, on_delete=models.CASCADE)
    producto = models.ForeignKey(Producto, on_delete=models.PROTECT)
    cantidad = models.IntegerField()
    precio_unitario = models.DecimalField(max_digits=10, decimal_places=2)
    subtotal = models.DecimalField(max_digits=10, decimal_places=2)
    def __str__(self):
        return f"Detalle de Venta {self.venta.id}"

