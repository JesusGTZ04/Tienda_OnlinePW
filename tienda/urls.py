from django.urls import path
from django.urls import include
from myapp.views import *

urlpatterns = [
    path('crear_usuario/', create_usuario, name='crear_usuario'),
    path('main/', main_view, name='main_view'),
    path('', index, name='index'),
    path('admin_main/', admin_main, name='admin_main'),
    path('add_articulo/', add_articulo, name='add_articulo'),
    
]
