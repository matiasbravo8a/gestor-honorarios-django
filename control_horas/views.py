from django.shortcuts import render
from django.utils.timezone import now
from .models import RegistroTurno

def dashboard(request):
    hoy = now() # Obtenemos la fecha de hoy
    
    # Filtramos solo los turnos del mes actual
    turnos_del_mes = RegistroTurno.objects.filter(
        fecha__year=hoy.year,
        fecha__month=hoy.month
    ).order_by('-fecha')
    
    # Calculamos los totales
    total_dinero = sum(turno.total_ganado for turno in turnos_del_mes)
    total_horas = sum(turno.horas_trabajadas for turno in turnos_del_mes)
    
    # Empaquetamos todo para enviarlo al HTML
    contexto = {
        'turnos': turnos_del_mes,
        'total_dinero': total_dinero,
        'total_horas': total_horas,
    }
    
    return render(request, 'control_horas/dashboard.html', contexto)