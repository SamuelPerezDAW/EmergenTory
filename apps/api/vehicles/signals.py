from django.db.models.signals import post_save
from django.dispatch import receiver

from checklists.models import Checklist

from .models import Vehicle


@receiver(post_save, sender=Vehicle)
def create_checklist(sender, instance, created, raw, using, update_fields, **kwargs):
    if created:
        Checklist.objects.create(usuario=instance.usuario, vehiculo=instance.vehiculo)
