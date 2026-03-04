import json

from django.db import IntegrityError
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

from shared.decorators import require_admin, require_http_methods
from users.decorators import auth_required

from .models import Checkitem, Checklist
from .serializers import CheckitemSerializer, ChecklistSerializer


@csrf_exempt
@require_http_methods('GET')
def checklists_list(request):
    usuario = request.GET.get('usuario')
    vehiculo = request.GET.get('vehiculo')
    creado = request.GET.get('creado')
    actualizado = request.GET.get('actualizado')
    checklists = Checklist.objects.all()

    if usuario:
        checklists = checklists.filter(usuario__username=usuario)

    if vehiculo:
        checklists = checklists.filter(vehiculo__matricula=vehiculo)

    if creado:
        checklists = checklists.filter(creado=creado)

    if actualizado:
        checklists = checklists.filter(actualizado=actualizado)

    serializer = ChecklistSerializer(checklists, request=request)
    return serializer.json_response()


@csrf_exempt
@require_http_methods('GET')
def checkitems_list(request):
    nombre = request.GET.get('nombre')
    activo = request.GET.get('activo')
    checklist = request.GET.get('checklist')
    checkitems = Checkitem.objects.all()

    if nombre:
        checkitems = checkitems.filter(nombre=nombre)

    if activo:
        checkitems = checkitems.filter(activo=activo)

    if checklist:
        checkitems = checkitems.filter(checklist__vehiculo__matricula=checklist)

    serializer = CheckitemSerializer(checkitems, request=request)
    return serializer.json_response()


@csrf_exempt
@require_http_methods('POST')
@auth_required
@require_admin
def add_item(request):
    try:
        payload = json.loads(request.body)

        if 'nombre' not in payload:
            return JsonResponse({'error': 'Falta el campo nombre'}, status=400)

        elif len(payload['nombre']) > 255:
            return JsonResponse(
                {'error': 'Nombre solo puede tener hasta 255 carácteres'}, status=400
            )

        if 'activo' not in payload:
            return JsonResponse({'error': 'Falta el campo activo'}, status=400)

        if not isinstance(payload['activo'], bool):
            raise json.JSONDecodeError('', '', 0)

        if 'checklist' not in payload:
            return JsonResponse(
                {'error': 'El campo checklist no contiene una matricula'}, status=400
            )

        if Checkitem.objects.filter(
            nombre=payload['nombre'], checklist__vehiculo__matricula=payload['checklist']
        ):
            raise IntegrityError()

        checklist = Checklist.objects.get(vehiculo__matricula=payload['checklist'])

        checkitem = Checkitem.objects.create(
            nombre=payload['nombre'],
            activo=payload['activo'],
            checklist=checklist,
        )

    except json.JSONDecodeError:
        return JsonResponse({'error': 'Json inválido'}, status=400)

    except IntegrityError:
        return JsonResponse({'error': 'El item para esa lista ya existe'}, status=400)

    except Checklist.DoesNotExist:
        return JsonResponse({'error': 'La lista no existe'}, status=404)

    return JsonResponse({'id': checkitem.pk})


@csrf_exempt
@require_http_methods('POST')
@auth_require
@require_admin
def mod_item(request, matricula, nombre_item):
    try:
        payload = json.loads(request.body)
        checklist = Checklist.objects.get(vehiculo__matricula=matricula)

        if 'activo' not in payload:
            return JsonResponse({'error': 'Falta el campo activo'}, status=400)

        if not isinstance(payload['activo'], bool):
            raise json.JSONDecodeError('', '', 0)

        Checkitem.objects.filter(
            nombre=nombre_item, checklist__vehiculo__matricula=checklist
        ).update(
            activo=payload['activo'],
        )

        item = Checkitem.objects.get(nombre=nombre_item, checklist__vehiculo__matricula=checklist)

    except json.JSONDecodeError:
        return JsonResponse({'error': 'Json inválido'}, status=400)

    except Checkitem.DoesNotExist:
        return JsonResponse({'error': 'Item no encontrado'}, status=404)

    except Checklist.DoesNotExist:
        return JsonResponse({'error': 'Lista no encontrada'}, status=404)

    return JsonResponse({'id': item.pk, 'nombre': item.nombre, 'activo': item.activo})


@csrf_exempt
@require_http_methods('POST')
@auth_required
@require_admin
def del_item(request, matricula, nombre_item):
    try:
        checklist = Checklist.objects.get(vehiculo__matricula=matricula)
        Checkitem.objects.get(nombre=nombre_item, checklist__vehiculo__matricula=checklist)

        item = Checkitem.objects.filter(
            nombre=nombre_item, checklist__vehiculo__matricula=checklist
        ).delete()

    except Checkitem.DoesNotExist:
        return JsonResponse({'error': 'Item no encontrado'}, status=404)

    except Checklist.DoesNotExist:
        return JsonResponse({'error': 'Lista no encontrada'}, status=404)

    return JsonResponse({'id': item})
