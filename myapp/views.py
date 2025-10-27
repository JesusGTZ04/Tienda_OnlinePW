from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import *

# Create your views here.
def main_view(request):
    return render(request, 'main.html')

def create_usuario(request):
    if request.method == 'POST':
        nombre = request.POST.get('nombre')
        apellidop = request.POST.get('apellidoP')
        apellidom = request.POST.get('apellidoM')
        telefono = request.POST.get('numero')
        correo = request.POST.get('email')
        contrasenia = request.POST.get('password')
        

        usuario = Usuarios(
            nombre=nombre,
            apellidop=apellidop,
            apellidom=apellidom,
            telefono=telefono,
            correo=correo,
            contrasenia=contrasenia
        )
        usuario.save()
        return redirect('crear_usuario')  

    return render(request, 'main.html')

def index(request):
    return render(request, 'index.html')

def admin_view(request):
    return render(request, 'admin.html')

def admin_main(request):
    #articulos = Articulos.objects.all()
    return render(request, 'admin_main.html')

def add_articulo(request):
    """if request.method == 'POST':
        nombre = request.POST.get('nombre')
        descripcion = request.POST.get('descripcion')
        precio = request.POST.get('precio')
        categoria = request.POST.get('categoria')
        stock = request.POST.get('stock')

        articulo = Articulos(
            nombre=nombre,
            descripcion=descripcion,
            precio=precio,
            categoria=categoria,
            stock=stock
        )
        articulo.save()
        return redirect('admin_main')
    """
    return render(request, 'add_articulo.html')

def inicio_sesion(request):
    return render(request, 'inicio_sesion.html')

def registro(request):
    return render(request, 'registro.html')