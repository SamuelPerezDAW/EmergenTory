from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.mail import send_mail
from django_rq import job


@job
def send_reset_password_email(user_id, uid, token) -> None:
    user = get_user_model().objects.get(pk=user_id)
    reset_url = f'{settings.FRONTEND_URL}/reset-password/{uid}/{token}'

    send_mail(
        'Restablecer contraseña en EmergenTory',
        (
            'Has solicitado restablecer tu contraseña en EmergenTory.\n\n'
            f'Usa este enlace para crear una nueva contraseña:\n{reset_url}\n\n'
            'Si no has solicitado este cambio, puedes ignorar este mensaje.'
        ),
        settings.DEFAULT_FROM_EMAIL,
        [user.email],
        fail_silently=False,
    )
