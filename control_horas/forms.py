from django import forms
from .models import RegistroTurno

class RegistroTurnoForm(forms.ModelForm):
    class Meta:
        model = RegistroTurno
        # Solo pedimos estos 3 campos (el total de dinero se calcula solo)
        fields = ['establecimiento', 'fecha', 'horas_trabajadas'] 
        
        # Le inyectamos los estilos de Tailwind a cada cajita de texto
        widgets = {
            'establecimiento': forms.Select(attrs={'class': 'w-full p-2 border border-gray-300 rounded-md bg-white text-sm'}),
            'fecha': forms.DateInput(attrs={'type': 'date', 'class': 'w-full p-2 border border-gray-300 rounded-md bg-white text-sm'}),
            'horas_trabajadas': forms.NumberInput(attrs={'class': 'w-full p-2 border border-gray-300 rounded-md bg-white text-sm', 'step': '0.5', 'placeholder': 'Ej: 8.5'}),
        }