from django.shortcuts import render, redirect
from django.utils.timezone import now
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from .models import RegistroTurno
from .forms import RegistroTurnoForm

# Vista para crear una cuenta nueva
def registro(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user) # Inicia sesión automáticamente tras registrarse
            return redirect('dashboard')
    else:
        form = UserCreationForm()
    return render(request, 'control_horas/registro.html', {'form': form})


# El candado: Si no estás logueado, te manda al Login
@login_required 
def dashboard(request):
    if request.method == 'POST':
        form = RegistroTurnoForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('dashboard')
    else:
        # Filtramos para que en el selector solo salgan los lugares del usuario actual
        form = RegistroTurnoForm()
        form.fields['establecimiento'].queryset = form.fields['establecimiento'].queryset.filter(profesional=request.user)

    hoy = now()
    
    # ¡Clave! Filtramos por mes, año Y por el usuario logueado (request.user)
    turnos_del_mes = RegistroTurno.objects.filter(
        establecimiento__profesional=request.user,
        fecha__year=hoy.year,
        fecha__month=hoy.month
    ).order_by('-fecha')
    
    total_dinero = sum(turno.total_ganado for turno in turnos_del_mes)
    total_horas = sum(turno.horas_trabajadas for turno in turnos_del_mes)
    
    contexto = {
        'turnos': turnos_del_mes,
        'total_dinero': total_dinero,
        'total_horas': total_horas,
        'form': form,
    }
    return render(request, 'control_horas/dashboard.html', contexto)
@login_required
def perfil(request):
    return render(request, 'control_horas/perfil.html')