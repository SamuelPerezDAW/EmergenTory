import json

from django.contrib.auth import get_user_model, hashers
from django.core.exceptions import ValidationError
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

    except ValidationError:
        return JsonResponse({'error': 'Formato inválido de teléfono'}, status=400)

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
        usuario = get_user_model().objects.get(username=nombre_usuario)

        perfil_validar = Profile.objects.get(usuario=token.usuario)
        perfil_original = Profile.objects.get(usuario__username=nombre_usuario)

        if Profile.objects.get(usuario=token.usuario).admin:
            usuario = get_user_model().objects.filter(username=nombre_usuario).delete()

        elif perfil_original == perfil_validar:
            usuario = get_user_model().objects.filter(username=nombre_usuario).delete()

        else:
            return JsonResponse({'error': 'No tienes permisos para esta operación'}, status=403)

    except Token.DoesNotExist:
        return JsonResponse({'error': 'Token no existe'}, status=404)

    except Profile.DoesNotExist:
        return JsonResponse({'error': 'Perfil no existe'}, status=404)
    except get_user_model().DoesNotExist:
        return JsonResponse({'error': 'Usuario no encontrado'}, status=404)

    return JsonResponse({'id': usuario})


@csrf_exempt
@require_http_methods('POST')
@auth_required
def mod_profile(request, nombre_usuario):
    try:
        payload = json.loads(request.body)
        bearer_token = request.headers.get('Authorization', '')
        token = Token.objects.get(key=bearer_token.split('Bearer ')[1])

        perfil_validar = Profile.objects.get(usuario=token.usuario)
        perfil_original = Profile.objects.get(usuario__username=nombre_usuario)
        mod_user = get_user_model().objects.filter(username=nombre_usuario)
        mod_profile = Profile.objects.filter(usuario__username=nombre_usuario)
        data = {'actualizados': []}

        # En caso de que el usuario que está haciendo la petición tenga el rol de admin, se le permite hacerlo.
        # En caso contrario se comprueba que el usuario sea el propietario.
        if Profile.objects.get(usuario=token.usuario).admin:
            if 'nombre_usuario' in payload:
                if get_user_model().objects.filter(username=payload['nombre_usuario']):
                    return JsonResponse({'error': 'El usuario ya existe'}, status=400)

                data['actualizados'] += {'id': mod_user.update(username=payload['nombre_usuario'])}

            if 'nombre' in payload:
                data['actualizados'] += {'id': mod_user.update(first_name=payload['nombre'])}

            if 'apellidos' in payload:
                data['actualizados'] += {'id': mod_user.update(last_name=payload['apellidos'])}

            if 'email' in payload:
                data['actualizados'] += {'id': mod_user.update(email=payload['email'])}

            if 'bio' in payload:
                data['actualizados'] += {'id': mod_profile.update(bio=payload['bio'])}

            if 'avatar' in payload:
                data['actualizados'] += {'id': mod_profile.update(avatar=payload['avatar'])}

            if 'telefono' in payload:
                profile_phone = mod_profile.first()
                profile_phone.telefono = payload['telefono']
                profile_phone.full_clean()
                profile_phone.save()
                data['actualizados'] += {'id': mod_profile.first().pk}

        elif perfil_original == perfil_validar:
            if 'nombre_usuario' in payload:
                if get_user_model().objects.filter(username=payload['nombre_usuario']):
                    return JsonResponse({'error': 'El usuario ya existe'}, status=400)

                data['actualizados'] += {'id': mod_user.update(username=payload['nombre_usuario'])}

            if 'nombre' in payload:
                data['actualizados'] += {'id': mod_user.update(first_name=payload['nombre'])}

            if 'apellidos' in payload:
                data['actualizados'] += {'id': mod_user.update(last_name=payload['apellidos'])}

            if 'email' in payload:
                data['actualizados'] += {'id': mod_user.update(email=payload['email'])}

            if 'bio' in payload:
                data['actualizados'] += {'id': mod_profile.update(bio=payload['bio'])}

            if 'avatar' in payload:
                data['actualizados'] += {'id': mod_profile.update(avatar=payload['avatar'])}

            if 'telefono' in payload:
                mod_profile.first().telefono = payload['telefono']
                mod_profile.first().full_clean()
                mod_profile.first().save()
                data['actualizados'] += {'id': mod_profile.first().pk}

        else:
            return JsonResponse({'error': 'No tienes permisos para esta operación'}, status=403)

    except Token.DoesNotExist:
        return JsonResponse({'error': 'Token no existe'}, status=404)

    except ValidationError:
        return JsonResponse({'error': 'Teléfono no válido'}, status=400)

    except Profile.DoesNotExist:
        return JsonResponse({'error': 'Perfil no existe'}, status=404)

    except get_user_model().DoesNotExist:
        return JsonResponse({'error': 'Usuario no encontrado'}, status=404)

    return JsonResponse(data)


@csrf_exempt
@require_http_methods('POST')
@auth_required
def reset_password(request, nombre_usuario):
    try:
        payload = json.loads(request.body)
        bearer_token = request.headers.get('Authorization', '')
        token = Token.objects.get(key=bearer_token.split('Bearer ')[1])

        perfil_validar = Profile.objects.get(usuario=token.usuario)
        perfil_original = Profile.objects.get(usuario__username=nombre_usuario)
        mod_user = get_user_model().objects.filter(username=nombre_usuario)

        data = {'actualizados': []}
        if Profile.objects.get(usuario=token.usuario).admin:
            if 'contraseña' in payload:
                data['actualizados'] += {
                    'id': mod_user.update(
                        password=hashers.make_password(
                            payload['contraseña'], salt=None, hasher='default'
                        ),
                    )
                }

        elif perfil_original == perfil_validar:
            if 'contraseña' in payload:
                data['actualizados'] += {
                    'id': mod_user.update(
                        password=hashers.make_password(
                            payload['contraseña'], salt=None, hasher='default'
                        ),
                    )
                }

        else:
            return JsonResponse({'error': 'No tienes permisos para esta operación'}, status=403)

    except Token.DoesNotExist:
        return JsonResponse({'error': 'Token no existe'}, status=404)

    except ValidationError:
        return JsonResponse({'error': 'Teléfono no válido'}, status=400)

    except Profile.DoesNotExist:
        return JsonResponse({'error': 'Perfil no existe'}, status=404)

    except get_user_model().DoesNotExist:
        return JsonResponse({'error': 'Usuario no encontrado'}, status=404)

    return JsonResponse(data)
