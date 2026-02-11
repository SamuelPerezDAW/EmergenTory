import re

from django.http import JsonResponse

from .models import Profile, Token


def auth_required(func):
    # Bearer Token como UUID
    BEARER_TOKEN_REGEX = (
        r'Bearer (?P<token>[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12})'
    )

    def wrapper(request, *args, **kwargs):
        bearer_token = request.headers.get('Authorization', '')
        if not (m := re.fullmatch(BEARER_TOKEN_REGEX, bearer_token)):
            return JsonResponse({'error': 'Token inválido'}, status=400)
        try:
            token = Token.objects.get(key=m['token'])
        except Token.DoesNotExist:
            return JsonResponse({'error': 'Token no registrado'}, status=401)
        request.user = token.usuario
        return func(request, *args, **kwargs)

    return wrapper


def auth_profile(func):
    def wrapper(request, *args, **kwargs):
        try:
            bearer_token = request.headers.get('Authorization', '')
            token = Token.objects.get(key=bearer_token.split('Bearer ')[1])

            perfil_validar = Profile.objects.get(usuario=token.usuario)
            perfil_original = Profile.objects.get(usuario__username=kwargs.get('nombre_usuario'))

            if perfil_validar.usuario != perfil_original.usuario:
                return JsonResponse({'error': 'No tienes permisos para esta acción'}, status=403)

        except Token.DoesNotExist:
            return JsonResponse({'error': 'Token no existe'}, status=404)

        except Profile.DoesNotExist:
            return JsonResponse({'error': 'Perfil no existe'}, status=404)

        return func(request, *args, **kwargs)

    return wrapper
