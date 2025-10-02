from django.urls import path
from .views import main_view
from django.urls import include
from django.contrib import admin

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('tienda.urls'))
]

