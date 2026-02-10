import json

from django.core.exceptions import ValidationError
from django.db import IntegrityError
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

from shared.decorators import require_http_methods
from users.decorators import auth_required

from .models import Vehicle
from .serializers import VehicleSerializer


@csrf_exempt
@require_http_methods('GET')
def vehicle_list(request):
    matricula = request.GET.get('matricula')
    modelo = request.GET.get('modelo')
    marca = request.GET.get('marca')
    categoria = request.GET.get('categoria')
    vehicles = Vehicle.objects.all()

    if matricula:
        vehicles = vehicles.filter(matricula=matricula)

    if modelo:
        vehicles = vehicles.filter(modelo=modelo)

    if marca:
        vehicles = vehicles.filter(marca=marca)

    if categoria:
        vehicles = vehicles.filter(categoria=categoria)

    serializer = VehicleSerializer(vehicles, request=request)
    return serializer.json_response()


@csrf_exempt
@require_http_methods('POST')
@auth_required
def add_vehicle(request):
    try:
        payload = json.loads(request.body)

        if 'matricula' not in payload:
            return JsonResponse({'error': 'Falta el campo Matricula'}, status=400)

        if Vehicle.objects.filter(matricula=payload['matricula']):
            raise IntegrityError()

        if 'marca' not in payload:
            return JsonResponse({'error': 'Falta el campo Marca'}, status=400)

        if len(payload['marca']) > 200:
            return JsonResponse(
                {'error': 'Marca solo puede tener hasta 200 carácteres'}, status=400
            )

        if 'modelo' not in payload:
            return JsonResponse({'error': 'Falta el campo Modelo'}, status=400)

        if len(payload['modelo']) > 200:
            return JsonResponse(
                {'error': 'Modelo solo puede tener hasta 200 carácteres'}, status=400
            )

        if 'categoria' not in payload:
            payload['categoria'] = 'POL'

        if payload['categoria'] not in ['POL', 'BOM', 'AMB']:
            return JsonResponse({'error': 'La categoría no es válida'}, status=400)

        vehicle = Vehicle.objects.create(
            matricula=payload['matricula'],
            marca=payload['marca'],
            modelo=payload['modelo'],
            categoria=payload['categoria'],
        )

    except json.JSONDecodeError:
        return JsonResponse({'error': 'Json inválido'}, status=400)

    except IntegrityError:
        return JsonResponse({'error': 'El vehículo ya existe'}, status=400)

    except ValidationError as error:
        return JsonResponse({'error': str(error.message)}, status=400)

    return JsonResponse({'id': vehicle.pk})
