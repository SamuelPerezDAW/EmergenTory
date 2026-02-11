import json

from django.contrib.auth import get_user_model, hashers
from django.db import IntegrityError
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

from shared.decorators import require_admin, require_http_methods

from .decorators import auth_profile, auth_required
from .models import Profile, Token
from .serializers import ProfileSerializer


@csrf_exempt
@require_http_methods('GET')
@auth_required
@auth_profile
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
@require_admin
def add_user(request):
    try:
        payload = json.loads(request.body)

        if 'nombre_usuario' not in payload:
            return JsonResponse({'error': 'Falta el campo Nombre de usuario'}, status=400)
        elif len(payload['nombre_usuario'].split(' ')) > 1:
            return JsonResponse(
                {'error': 'El nombre de usuario no debe contener espacios'}, status=400
            )

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
            password=hashers.make_password(payload['contraseña'], salt=None, hasher='default'),
            first_name=payload['nombre'],
            last_name=payload['apellido'],
            email=payload['email'],
        )

    except json.JSONDecodeError:
        return JsonResponse({'error': 'Json inválido'}, status=400)

    except IntegrityError:
        return JsonResponse({'error': 'El usuario ya existe'}, status=400)
    return JsonResponse({'id': user.pk})


@csrf_exempt
@require_http_methods('POST')
@auth_required
def del_user(request, nombre_usuario):
    try:
        bearer_token = request.headers.get('Authorization', '')
        token = Token.objects.get(key=bearer_token.split('Bearer ')[1])
        get_user_model().objects.get(username=nombre_usuario)
        perfil_validar = Profile.objects.get(usuario=token.usuario)
        perfil_original = Profile.objects.get(usuario__username=nombre_usuario)
        # Añadir usuario admin y usuario propietario sin el auth
        usuario = get_user_model().objects.filter(username=nombre_usuario).delete()

    except Token.DoesNotExist:
        return JsonResponse({'error': 'Token no existe'}, status=404)

    except Profile.DoesNotExist:
        return JsonResponse({'error': 'Perfil no existe'}, status=404)
    except get_user_model().DoesNotExist:
        return JsonResponse({'error': 'Usuario no encontrado'}, status=404)

    return JsonResponse({'id': usuario})
