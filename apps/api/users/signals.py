from django.contrib.auth import get_user_model
from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import Profile, Token


@receiver(post_save, sender=get_user_model())
def create_user_profile(sender, instance, created, raw, using, update_fields, **kwargs):
    if created:
        Profile.objects.create(usuario=instance)


@receiver(post_save, sender=get_user_model())
def create_user_token(sender, instance, created, raw, using, update_fields, **kwargs):
    if created:
        Token.objects.create(usuario=instance)
