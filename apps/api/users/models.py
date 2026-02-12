import uuid

from django.conf import settings
from django.core.validators import RegexValidator
from django.db import models


class Profile(models.Model):
    avatar = models.ImageField(upload_to='avatars', default='avatars/noavatar.png')
    bio = models.TextField(blank=True)
    telefono = models.CharField(
        max_length=32,
        validators=[
            RegexValidator(
                regex=r'^\+?\d{1,4}?[-.\s]?\(?\d{1,3}?\)?[-.\s]?\d{1,4}[-.\s]?\d{1,4}[-.\s]?\d{1,9}$'
            )
        ],
        blank=True,
        null=True,
    )
    admin = models.BooleanField(default=False)
    usuario = models.OneToOneField(
        settings.AUTH_USER_MODEL, related_name='profile', on_delete=models.CASCADE
    )

    def __str__(self):
        return self.usuario.username


class Token(models.Model):
    key = models.UUIDField(unique=True, default=uuid.uuid4, editable=False)
    usuario = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    creado = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.key)
