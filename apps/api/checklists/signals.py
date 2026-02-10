from django.db.models.signals import post_delete, post_save
from django.dispatch import receiver

from vehicles.models import Vehicle

from .models import Checkitem, Checklist


@receiver(post_save, sender=Checkitem)
def update_checklist(sender, instance, created, raw, using, update_fields, **kwargs):
    if not created:
        instance.checklist.save()


@receiver(post_delete, sender=Checklist)
def delete_vehicles(sender, instance, using, origin, **kwargs):
    Vehicle.objects.filter(matricula=instance.vehiculo.matricula).delete()
