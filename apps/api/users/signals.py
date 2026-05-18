from django.contrib.auth import get_user_model
from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver

from .models import Profile, Token


@receiver(post_save, sender=get_user_model())
def create_user_profile(sender, instance, created, raw, using, update_fields, **kwargs):
    if created:
        if instance.pk == 1:
            Profile.objects.create(usuario=instance, admin=True)
        else:
            Profile.objects.create(usuario=instance)

@receiver(post_save, sender=get_user_model())
def create_user_token(sender, instance, created, raw, using, update_fields, **kwargs):
    if created:
        Token.objects.create(usuario=instance)


@receiver(pre_save, sender=Profile)
def phone_number_validation(sender, instance, raw, using, update_fields, **kwargs):
    return
