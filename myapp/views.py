from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import Usuarios

# Create your views here.
def main_view(request):
    return render(request, 'main.html')

def create_usuario(request):
    usu = Usuarios(nombre=request.POST['nombre'], apellidop = request.POST['apellidoP'], apellidom = request.POST['apellidoP'],
            telefono = request.POST['numero'], correo=request.POST['email'], contrasenia = request.POST['password'])
    usu.save()
    return redirect('/main/')


    