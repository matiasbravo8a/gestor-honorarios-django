from django import forms
from .models import RegistroTurno, Establecimiento

class RegistroTurnoForm(forms.ModelForm):
    class Meta:
        model = RegistroTurno
        # Solo pedimos estos 3 campos (el total de dinero se calcula solo)
        fields = ['establecimiento', 'fecha', 'horas_trabajadas', 'es_festivo'] 
        
        # Le inyectamos los estilos de Tailwind a cada cajita de texto
        widgets = {
            'establecimiento': forms.Select(attrs={'class': 'w-full p-2 border border-gray-300 rounded-md bg-white text-sm'}),
            'fecha': forms.DateInput(attrs={'type': 'date', 'class': 'w-full p-2 border border-gray-300 rounded-md bg-white text-sm'}),
            'horas_trabajadas': forms.NumberInput(attrs={'class': 'w-full p-2 border border-gray-300 rounded-md bg-white text-sm', 'step': '0.5', 'placeholder': 'Ej: 8.5'}),
            'es_festivo': forms.CheckboxInput(attrs={'class': 'h-4 w-4 text-emerald-600 border-gray-300 rounded'}),
        }
        # Formulario para la vista de Perfil
class EstablecimientoForm(forms.ModelForm):
    class Meta:
        model = Establecimiento
        # NUEVO: Agregamos 'valor_hora_festivo'
        fields = ['nombre', 'valor_hora', 'valor_hora_festivo']
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'w-full p-2 border rounded-md', 'placeholder': 'Ej: Hospital Collipulli'}),
            'valor_hora': forms.NumberInput(attrs={'class': 'w-full p-2 border rounded-md', 'placeholder': 'Ej: 15000'}),
            'valor_hora_festivo': forms.NumberInput(attrs={'class': 'w-full p-2 border rounded-md', 'placeholder': 'Ej: 20000 (Opcional)'}),
        }