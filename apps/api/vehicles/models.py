from django.contrib.auth import get_user_model
from django.db import models


class Vehicle(models.Model):
    matricula = models.CharField(max_length=7, unique=True, editable=False)
    marca = models.CharField(max_length=200)
    modelo = models.CharField(max_length=200)
    user = models.ManyToManyField(
        get_user_model(),
    )
