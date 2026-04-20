from django.urls import path
from . import views

urlpatterns = [
    # Esto conecta la ruta vacía ('') con nuestro panel de resumen
    path('', views.dashboard, name='dashboard'),
]