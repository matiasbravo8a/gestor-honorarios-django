from django.shortcuts import render, redirect
from django.utils.timezone import now
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required

# Agrupamos los modelos en una sola línea
from .models import RegistroTurno, Establecimiento

# Agrupamos los formularios en una sola línea (¡Aquí está la corrección!)
from .forms import EstablecimientoForm, RegistroTurnoForm

# Vista para crear una cuenta nueva...

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
        form = RegistroTurnoForm()
        form.fields['establecimiento'].queryset = form.fields['establecimiento'].queryset.filter(profesional=request.user)

    hoy = now()
    
    turnos_del_mes = RegistroTurno.objects.filter(
        establecimiento__profesional=request.user,
        fecha__year=hoy.year,
        fecha__month=hoy.month
    ).order_by('-fecha')
    
    # --- NUEVO DESGLOSE INTELIGENTE ---
    total_honorarios = sum(turno.total_ganado for turno in turnos_del_mes if turno.establecimiento.tipo_trabajo == 'HONORARIOS')
    total_extras = sum(turno.total_ganado for turno in turnos_del_mes if turno.establecimiento.tipo_trabajo == 'EXTRAS')
    
    total_dinero = total_honorarios + total_extras
    total_horas = sum(turno.horas_trabajadas for turno in turnos_del_mes)
    
    contexto = {
        'turnos': turnos_del_mes,
        'total_dinero': total_dinero,
        'total_honorarios': total_honorarios, # Pasamos el subtotal de honorarios
        'total_extras': total_extras,         # Pasamos el subtotal de extras
        'total_horas': total_horas,
        'form': form,
    }
    return render(request, 'control_horas/dashboard.html', contexto)
@login_required
def perfil(request):
    if request.method == 'POST':
        form = EstablecimientoForm(request.POST)
        if form.is_valid():
            # Creamos el objeto pero no lo guardamos aún
            lugar = form.save(commit=False)
            # Le asignamos el usuario que está logueado actualmente
            lugar.profesional = request.user
            lugar.save()
            return redirect('perfil')
    else:
        form = EstablecimientoForm()

    # Traemos solo los lugares creados por este usuario
    mis_lugares = Establecimiento.objects.filter(profesional=request.user).order_by('nombre')
    
    contexto = {
        'form': form,
        'mis_lugares': mis_lugares,
    }
    
    return render(request, 'control_horas/perfil.html', contexto)