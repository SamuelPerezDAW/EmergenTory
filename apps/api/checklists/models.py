from django.conf import settings
from django.db import models


class Checkitem(models.Model):
    name = models.CharField(max_length=255)
    active = models.BooleanField(default=False)


class Checklist(models.Model):
    user = models.ManyToManyField(settings.AUTH_USER_MODEL)
    vehicle = models.OneToOneField('vehicles.Vehicle', on_delete=models.CASCADE, unique=True)
    checkitem = models.ForeignKey(Checkitem, on_delete=models.DO_NOTHING)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
