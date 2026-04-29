from django.db import models
from django.contrib.auth.models import User

class Establecimiento(models.Model):
    TIPO_CHOICES = [
        ('HONORARIOS', 'Prestación de Servicios (Honorarios)'),
        ('EXTRAS', 'Contrato Fijo (Horas Extras)'),
    ]

    profesional = models.ForeignKey(User, on_delete=models.CASCADE)
    nombre = models.CharField(max_length=150, help_text="Ej: Clínica Centro, Empresa XYZ")
    
    # El selector de tipo de trabajo
    tipo_trabajo = models.CharField(max_length=20, choices=TIPO_CHOICES, default='HONORARIOS')
    
    valor_hora = models.DecimalField(max_digits=10, decimal_places=0, help_text="Valor por hora normal o Extra al 50%")
    valor_hora_festivo = models.DecimalField(max_digits=10, decimal_places=0, null=True, blank=True, help_text="Valor por hora festivo o Extra al 100%")
    
    def __str__(self):
        # Le agregamos una etiqueta visual al nombre
        tipo_label = "Honorarios" if self.tipo_trabajo == 'HONORARIOS' else "Horas Extras"
        return f"{self.nombre} ({tipo_label})"


class RegistroTurno(models.Model):
    # Django necesita que Establecimiento exista arriba para poder referenciarlo aquí
    establecimiento = models.ForeignKey(Establecimiento, on_delete=models.CASCADE)
    fecha = models.DateField()
    horas_trabajadas = models.DecimalField(max_digits=5, decimal_places=1, help_text="Cantidad de horas. Ej: 8.5")
    observaciones = models.TextField(blank=True, null=True)
    es_festivo = models.BooleanField(default=False, verbose_name="¿Es Domingo o Feriado?")

    @property
    def total_ganado(self):
        if self.es_festivo and self.establecimiento.valor_hora_festivo:
            return self.horas_trabajadas * self.establecimiento.valor_hora_festivo
        
        return self.horas_trabajadas * self.establecimiento.valor_hora

    def __str__(self):
        return f"{self.fecha} - {self.establecimiento.nombre} ({self.horas_trabajadas} hrs)"