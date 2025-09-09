from django.urls import path
from .views import main_view, create_usuario

urlpatterns = [
    path('', main_view),
    path('crear_usuario/', create_usuario),
]

