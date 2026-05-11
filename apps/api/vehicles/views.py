import json

from checklists.serializers import ChecklistSerializer
from django.core.exceptions import ValidationError
from django.db import IntegrityError
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from shared.decorators import require_admin, require_http_methods
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
    newVehicles = []

    for vehicle in vehicles:
        data = {
            'pk': vehicle.pk,
            'matricula': vehicle.matricula,
            'imagen': vehicle.imagen,
            'marca': vehicle.marca,
            'modelo': vehicle.modelo,
            'categoria': vehicle.categoria,
        }

        if not vehicle.checklist:
            data['lista'] = ''

        else:
            data['lista'] = (
                ChecklistSerializer(vehicle.checklist).serialize() if vehicle.checklist else '',
            )

        newVehicles.insert(0, data)

    vehicles = newVehicles

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
@require_admin
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


@csrf_exempt
@require_http_methods('POST')
@auth_required
@require_admin
def change_vehicle_image(request, matricula):
    try:
        payload = json.loads(request.body)

        vehicle = Vehicle.objects.filter(matricula=matricula)

        if not vehicle:
            return JsonResponse({'error': 'Vehiculo no encontrado'}, status=404)

        if 'imagen' in payload:
            vehicle.update(imagen=payload['imagen'])

        else:
            return JsonResponse({'error', 'Falta el campo imagen'}, status=400)

    except json.JSONDecodeError:
        return JsonResponse({'error': 'Json inválido'}, status=400)

    except ValidationError as error:
        return JsonResponse({'error': str(error.message)}, status=400)

    return JsonResponse({'id': vehicle})


@csrf_exempt
@require_http_methods('POST')
@auth_required
@require_admin
def del_vehicle(request, matricula):
    try:
        Vehicle.objects.get(matricula=matricula)

        vehicle = Vehicle.objects.filter(matricula=matricula).delete()

    except Vehicle.DoesNotExist:
        return JsonResponse({'error': 'Vehículo no encontrado'}, status=404)

    return JsonResponse({'id': vehicle})
