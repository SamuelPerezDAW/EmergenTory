import re

from django.core.exceptions import ValidationError
from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver

from checklists.models import Checklist

from .models import Vehicle


@receiver(post_save, sender=Vehicle)
def create_checklist(sender, instance, created, raw, using, update_fields, **kwargs):
    if created:
        Checklist.objects.create(vehiculo=instance)


@receiver(pre_save, sender=Vehicle)
def enrollment_auth(sender, instance, raw, using, update_fields, **kwargs):
    regex = r'^\d{4}[ -]?[BCDFGHJKLMNPQRSTVWXYZ]{3}$'

    if not re.match(regex, instance.matricula):
        raise ValidationError('Matrícula inválida')
