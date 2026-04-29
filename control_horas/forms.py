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
        fields = ['nombre', 'tipo_trabajo', 'valor_hora', 'valor_hora_festivo'] # <-- Asegúrate que esté aquí
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'w-full p-2.5 border border-gray-300 rounded-lg text-sm'}),
            'tipo_trabajo': forms.Select(attrs={'class': 'w-full p-2.5 border border-gray-300 rounded-lg text-sm bg-white'}),
            'valor_hora': forms.NumberInput(attrs={'class': 'w-full p-2.5 border border-gray-300 rounded-lg text-sm'}),
            'valor_hora_festivo': forms.NumberInput(attrs={'class': 'w-full p-2.5 border border-gray-300 rounded-lg text-sm'}),
        }