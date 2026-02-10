from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import Checkitem


@receiver(post_save, sender=Checkitem)
def update_checklist(sender, instance, created, raw, using, update_fields, **kwargs):
    if not created:
        instance.checklist.save()
