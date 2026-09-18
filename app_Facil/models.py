# en tu_app/models.py
from django.db import models

class Temblor(models.Model):
    magnitud = models.FloatField()
    lugar = models.CharField(max_length=200)
    fecha = models.DateField()
    hora = models.TimeField()
    profundidad = models.FloatField(help_text="Profundidad exacta en km")
    rango_profundidad = models.CharField(max_length=50)

    def __str__(self):
        return f"M{self.magnitud} - {self.lugar} ({self.fecha} {self.hora})"