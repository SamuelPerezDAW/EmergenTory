from django.contrib.auth import get_user_model
from django.db import models


class Checklist(models.Model):
    usuario = models.ManyToManyField(get_user_model(), related_name='checklists')
    vehiculo = models.OneToOneField(
        'vehicles.Vehicle', related_name='checklist', on_delete=models.CASCADE, unique=True
    )
    creado = models.DateTimeField(auto_now_add=True)
    actualizado = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.vehiculo.matricula


class Checkitem(models.Model):
    nombre = models.CharField(max_length=255)
    activo = models.BooleanField(default=False)
    checklist = models.ForeignKey(Checklist, related_name='checkitems', on_delete=models.CASCADE)

    def __str__(self):
        return self.nombre
