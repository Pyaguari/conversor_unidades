from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404
from .models import Especialidad, Magnitud, Unidad
from .utils import CONVERSION_FUNCTIONS
from decimal import Decimal, InvalidOperation

def seleccionar_magnitud(request):
    especialidades = Especialidad.objects.prefetch_related('magnitudes__unidades').all()
    return render(request, "conversor/seleccionar_magnitud.html", {
        "especialidades": especialidades
    })

def convertir_view(request, magnitud_id):
    magnitud = get_object_or_404(Magnitud.objects.prefetch_related('unidades'), id=magnitud_id)
    unidades = magnitud.unidades.all()  # ← AGREGAR ESTA LÍNEA
    
    context = {
        'magnitud': magnitud,
        'unidades': unidades,  # ← AGREGAR ESTA LÍNEA
        'resultado': None,
        'error': None,
        'valor': None,
        'unidad_origen_sel': None,
        'unidad_destino_sel': None,
        'unidad_origen_id': None,
        'unidad_destino_id': None,
    }
    
    if request.method == 'POST':
        try:
            valor = Decimal(request.POST.get('valor', '0'))
            unidad_origen_id = int(request.POST.get('unidad_origen'))
            unidad_destino_id = int(request.POST.get('unidad_destino'))
            
            unidad_origen = get_object_or_404(Unidad, id=unidad_origen_id, magnitud=magnitud)
            unidad_destino = get_object_or_404(Unidad, id=unidad_destino_id, magnitud=magnitud)
            
            # Obtener función de conversión
            conversion_fn = CONVERSION_FUNCTIONS.get(magnitud.codigo_calculo)
            
            if not conversion_fn:
                context['error'] = f"No existe conversión para {magnitud.nombre}"
            else:
                resultado = conversion_fn(
                    valor,
                    unidad_origen.simbolo,
                    unidad_destino.simbolo
                )
                
                context.update({
                    'resultado': round(resultado, 4),  # ← Redondear a 4 decimales
                    'valor': valor,
                    'unidad_origen_sel': unidad_origen,  # ← Cambiar nombre
                    'unidad_destino_sel': unidad_destino,  # ← Cambiar nombre
                    'unidad_origen_id': unidad_origen_id,
                    'unidad_destino_id': unidad_destino_id,
                })
                
        except (ValueError, InvalidOperation):
            context['error'] = "Por favor ingresa un valor numérico válido"
        except Exception as e:
            context['error'] = f"Error en la conversión: {str(e)}"
    
    return render(request, "conversor/convertir.html", context)


def debug_magnitud(request, magnitud_id):
    """Vista temporal para debug"""
    magnitud = get_object_or_404(Magnitud, id=magnitud_id)
    unidades = list(magnitud.unidades.values('id', 'nombre', 'simbolo'))
    
    return JsonResponse({
        'magnitud': magnitud.nombre,
        'codigo_calculo': magnitud.codigo_calculo,
        'total_unidades': magnitud.unidades.count(),
        'unidades': unidades
    })