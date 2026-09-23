from django.db import models

# ==========================================
# MODELO 1: Departamento (Lado 1 de la relación 1-N)
# ==========================================
class Departamento(models.Model):
    nombre = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.nombre


# ==========================================
# MODELO 2: Temblor (Lado N de 1-N)
# ==========================================
class Temblor(models.Model):
    magnitud = models.FloatField()
    lugar = models.CharField(max_length=150)
    fecha = models.DateField()
    hora = models.TimeField()
    profundidad = models.FloatField()
    rango_profundidad = models.CharField(max_length=50)

    # RELACIÓN 1 a N: ForeignKey apuntando a Departamento
    departamento = models.ForeignKey(
        Departamento, 
        on_delete=models.CASCADE, 
        related_name='temblores',
        null=True, 
        blank=True
    )

    def __str__(self):
        return f"Temblor M{self.magnitud} - {self.lugar}"


# ==========================================
# MODELO 3: ReporteDanios (RELACIÓN 1 a 1)
# ==========================================
class ReporteDanios(models.Model):
    # OneToOneField asegura que cada temblor solo tenga UN reporte asociado
    temblor = models.OneToOneField(
        Temblor, 
        on_delete=models.CASCADE, 
        primary_key=True,
        related_name='reporte_danios'
    )
    afectados = models.IntegerField(default=0)
    descripcion_danios = models.TextField()

    def __str__(self):
        return f"Reporte del temblor ID #{self.temblor.id}"