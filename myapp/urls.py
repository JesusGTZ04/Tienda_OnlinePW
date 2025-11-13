from django.urls import path
from .views import *
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', index, name="index"),
    path('articulos/', admin_main, name="articulos"),
    path('add_articulo/', add_articulo, name="add_articulo" ),
    path('inicioSesion/', inicio_sesion, name="inicio_sesion"),
    path('registro/', registro_usuario, name="registro"),
    path('cerrar_sesion/', cerrar_sesion, name="cerrar_sesion"),
    path('add/<int:producto_id>/', add_cart, name="add_carrito"),
    path('carrito/', view_cart, name="carrito"),
    path('carrito/eliminar/<int:producto_id>/', remove_cart, name='remove_cart'),
    path('usuarios/', admin_usuarios, name="usuarios"),
    path('perfil/editar/', editar_perfil, name='editar_perfil'),
    path('usuarios/eliminar/<int:user_id>/', eliminar_usuario, name="eliminar_usuario"),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
