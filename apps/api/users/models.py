import uuid

from django.conf import settings
from django.db import models
from phonenumber_field.modelfields import PhoneNumberField


class Profile(models.Model):
    avatar = models.ImageField(upload_to='avatars', default='avatars/noavatar.png')
    bio = models.TextField(blank=True)
    phone_number = PhoneNumberField(region='ES', blank=True, null=True)
    admin = models.BooleanField(default=False)
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL, related_name='profile', on_delete=models.CASCADE
    )

    def __str__(self):
        return self.user.username


class Token(models.Model):
    key = models.UUIDField(unique=True, default=uuid.uuid4, editable=False)
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.key)
