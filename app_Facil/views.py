from django.shortcuts import render, redirect
from .models import Temblor

def temblor(request):
    return render(request, 'temblor.html')

# Muestra SOLO el temblor que se acaba de registrar
def salida_temblor(request):
    if request.method == 'POST':
        magnitud = request.POST.get('magnitud')
        lugar = request.POST.get('lugar')
        fecha = request.POST.get('fecha')
        hora = request.POST.get('hora')
        profundidad = request.POST.get('profundidad')
        rango_profundidad = request.POST.get('rango_profundidad')

        # Guardar en la base de datos SQLite
        nuevo_temblor = Temblor.objects.create(
            magnitud=float(magnitud),
            lugar=lugar,
            fecha=fecha,
            hora=hora,
            profundidad=float(profundidad),
            rango_profundidad=rango_profundidad
        )

        return render(request, 'salida-temblor.html', {'temblor': nuevo_temblor})

    return redirect('formulario_temblor')

# Muestra TODOS los temblores guardados en SQLite
def lista_temblores(request):
    todos_los_temblores = Temblor.objects.all().order_by('-id')
    return render(request, 'salida-temblor.html', {'temblores': todos_los_temblores})

def buscar_temblor(request):
    busqueda = request.GET.get('busqueda')
    fecha_busqueda = request.GET.get('fecha_busqueda')
    hora_busqueda = request.GET.get('hora_busqueda')
    
    temblor_encontrado = None
    error = None

    # 1. Búsqueda por Fecha (y opcionalmente Hora)
    if fecha_busqueda:
        if hora_busqueda:
            temblor_encontrado = Temblor.objects.filter(fecha=fecha_busqueda, hora=hora_busqueda).first()
        else:
            temblor_encontrado = Temblor.objects.filter(fecha=fecha_busqueda).first()
        
        if not temblor_encontrado:
            error = f"No se encontró temblor registrado para la fecha {fecha_busqueda}" + (f" a las {hora_busqueda}" if hora_busqueda else "")

    # 2. Búsqueda por ID o Lugar
    elif busqueda:
        if busqueda.isdigit():
            temblor_encontrado = Temblor.objects.filter(id=int(busqueda)).first()
        else:
            temblor_encontrado = Temblor.objects.filter(lugar__icontains=busqueda).first()

        if not temblor_encontrado:
            error = f"No se encontró ningún temblor con la búsqueda: '{busqueda}'"

    return render(request, 'salida-temblor.html', {
        'temblor': temblor_encontrado,
        'error_busqueda': error
    })