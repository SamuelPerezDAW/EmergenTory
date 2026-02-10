from django.contrib.auth import get_user_model
from django.db import models


class Vehicle(models.Model):
    class Category(models.TextChoices):
        POLICIA = 'POL'
        AMBULANCIA = 'AMB'
        BOMBERO = 'BOM'

    matricula = models.CharField(max_length=7, unique=True, editable=False)
    marca = models.CharField(max_length=200)
    modelo = models.CharField(max_length=200)
    usuario = models.ManyToManyField(
        get_user_model(),
        related_name='vehicles',
    )
    categoria = models.CharField(max_length=3, choices=Category, default=Category.POLICIA)
