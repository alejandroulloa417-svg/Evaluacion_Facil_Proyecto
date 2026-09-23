from django.shortcuts import render, redirect
from .models import Temblor, Departamento, ReporteDanios

# 1. Muestra el formulario y carga la lista de Departamentos para el <select> (Relación 1-N)
def temblor(request):
    departamentos = Departamento.objects.all().order_by('nombre')
    return render(request, 'temblor.html', {'departamentos': departamentos})

# 2. Guarda el Temblor, su Departamento (1-N) y opcionalmente su Reporte de Daños (1-1)
def salida_temblor(request):
    if request.method == 'POST':
        magnitud = request.POST.get('magnitud')
        lugar = request.POST.get('lugar')
        fecha = request.POST.get('fecha')
        hora = request.POST.get('hora')
        profundidad = request.POST.get('profundidad')
        rango_profundidad = request.POST.get('rango_profundidad')

        # Datos de relaciones
        departamento_id = request.POST.get('departamento_id')
        afectados = request.POST.get('afectados')
        descripcion_danios = request.POST.get('descripcion_danios')

        # Obtener la instancia del departamento (1-N)
        departamento_obj = None
        if departamento_id:
            departamento_obj = Departamento.objects.filter(id=departamento_id).first()

        # Guardar el temblor en la base de datos SQLite
        nuevo_temblor = Temblor.objects.create(
            magnitud=float(magnitud),
            lugar=lugar,
            fecha=fecha,
            hora=hora,
            profundidad=float(profundidad),
            rango_profundidad=rango_profundidad,
            departamento=departamento_obj  # Asignación de ForeignKey (1-N)
        )

        # Guardar el Reporte de Daños (1-1)
        if descripcion_danios or afectados:
            ReporteDanios.objects.create(
                temblor=nuevo_temblor,  # Asignación de OneToOneField (1-1)
                afectados=int(afectados) if afectados else 0,
                descripcion_danios=descripcion_danios
            )

        return render(request, 'salida-temblor.html', {'temblor': nuevo_temblor})

    return redirect('formulario_temblor')

# 3. Muestra TODOS los temblores guardados
def lista_temblores(request):
    # select_related optimiza las consultas SQL para las relaciones 1-1 y 1-N
    todos_los_temblores = Temblor.objects.select_related('departamento', 'reporte_danios').all().order_by('-id')
    return render(request, 'salida-temblor.html', {'temblores': todos_los_temblores})

# 4. Búsqueda por ID, Lugar o Fecha/Hora
def buscar_temblor(request):
    busqueda = request.GET.get('busqueda')
    fecha_busqueda = request.GET.get('fecha_busqueda')
    hora_busqueda = request.GET.get('hora_busqueda')
    
    temblor_encontrado = None
    error = None

    # 1. Búsqueda por Fecha (y opcionalmente Hora)
    if fecha_busqueda:
        queryset = Temblor.objects.select_related('departamento', 'reporte_danios').filter(fecha=fecha_busqueda)
        if hora_busqueda:
            queryset = queryset.filter(hora=hora_busqueda)
        
        temblor_encontrado = queryset.first()
        
        if not temblor_encontrado:
            error = f"No se encontró temblor registrado para la fecha {fecha_busqueda}" + (f" a las {hora_busqueda}" if hora_busqueda else "")

    # 2. Búsqueda por ID o Lugar
    elif busqueda:
        queryset = Temblor.objects.select_related('departamento', 'reporte_danios')
        if busqueda.isdigit():
            temblor_encontrado = queryset.filter(id=int(busqueda)).first()
        else:
            temblor_encontrado = queryset.filter(lugar__icontains=busqueda).first()

        if not temblor_encontrado:
            error = f"No se encontró ningún temblor con la búsqueda: '{busqueda}'"

    return render(request, 'salida-temblor.html', {
        'temblor': temblor_encontrado,
        'error_busqueda': error
    })