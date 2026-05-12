from http import HTTPStatus

from django.http import JsonResponse
from users.models import Profile, Token


def require_http_methods(*methods):
    def decorator(func):
        def wrapper(request, *args, **kwargs):
            if request.method not in methods:
                return JsonResponse(
                    {'error': 'Metodo no permitido'},
                    status=HTTPStatus.METHOD_NOT_ALLOWED,
                )
            return func(request, *args, **kwargs)

        return wrapper

    return decorator


def require_admin(func):
    def wrapper(request, *args, **kwargs):
        try:
            bearer_token = request.headers.get('Authorization', '')
            token = Token.objects.get(key=bearer_token.split('Bearer ')[1])
            perfil = Profile.objects.get(usuario=token.usuario)
            if not perfil.admin:
                return JsonResponse({'error': 'No tienes permisos para esta acción'}, status=403)
        except Token.DoesNotExist:
            return JsonResponse({'error': 'Token no existe'}, status=404)

        except Profile.DoesNotExist:
            return JsonResponse({'error': 'Perfil no existe'}, status=404)
        return func(request, *args, **kwargs)

    return wrapper
