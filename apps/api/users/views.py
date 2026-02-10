import json

from django.contrib.auth import get_user_model
from django.db import IntegrityError
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

from shared.decorators import require_http_methods

from .decorators import auth_required
from .models import Profile
from .serializers import ProfileSerializer


@csrf_exempt
@require_http_methods('GET')
@auth_required
def user_profile(request, nombre_usuario: str):
    try:
        profile = Profile.objects.get(usuario__username=nombre_usuario)

    except Profile.DoesNotExist:
        return JsonResponse({'error': 'Perfil no encontrado'}, status=404)

    serializer = ProfileSerializer(profile, request=request)

    return serializer.json_response()


@csrf_exempt
@require_http_methods('POST')
@auth_required
def add_user(request):
    try:
        payload = json.loads(request.body)

        if 'nombre_usuario' not in payload:
            return JsonResponse({'error': 'Falta el campo Nombre de usuario'}, status=400)

        if 'contraseña' not in payload:
            return JsonResponse({'error': 'Falta el campo Contraseña'}, status=400)

        if get_user_model().objects.filter(username=payload['nombre_usuario']):
            raise IntegrityError()

        if 'nombre' not in payload:
            payload['nombre'] = ''

        if 'apellido' not in payload:
            payload['apellido'] = ''

        if 'email' not in payload:
            payload['email'] = ''

        user = get_user_model().objects.create(
            username=payload['nombre_usuario'],
            password=payload['contraseña'],
            first_name=payload['nombre'],
            last_name=payload['apellido'],
            email=payload['email'],
        )

    except json.JSONDecodeError:
        return JsonResponse({'error': 'Json inválido'}, status=400)

    except IntegrityError:
        return JsonResponse({'error': 'El usuario ya existe'}, status=400)
    # make_password(password, salt=None, hasher='default')[source]¶
    return JsonResponse({'id': user.pk})
