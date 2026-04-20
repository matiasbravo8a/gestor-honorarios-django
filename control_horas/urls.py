from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [

    # Esto conecta la ruta vacía ('') con nuestro panel de resumen
    path('', views.dashboard, name='dashboard'),
    path('registro/', views.registro, name='registro'),
    path('login/', auth_views.LoginView.as_view(template_name='control_horas/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    
]