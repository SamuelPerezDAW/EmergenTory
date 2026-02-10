from django.contrib.auth import get_user_model
from django.db import models


class Checkitem(models.Model):
    nombre = models.CharField(max_length=255)
    activo = models.BooleanField(default=False)


class Checklist(models.Model):
    usuario = models.ManyToManyField(get_user_model(), related_name='checklists')
    vehiculo = models.OneToOneField(
        'vehicles.Vehicle', related_name='checklist', on_delete=models.CASCADE, unique=True
    )
    item = models.ForeignKey(
        Checkitem, related_name='checklists', on_delete=models.DO_NOTHING, blank=True, null=True
    )
    creado = models.DateTimeField(auto_now_add=True)
    actualizado = models.DateTimeField(auto_now=True)
