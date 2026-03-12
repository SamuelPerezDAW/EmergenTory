from django.db import models


class Vehicle(models.Model):
    class Category(models.TextChoices):
        POLICIA = 'POL'
        AMBULANCIA = 'AMB'
        BOMBERO = 'BOM'

    matricula = models.CharField(max_length=7, unique=True)
    imagen = models.ImageField(
        upload_to='imagenes_vehiculos',
        default='imagenes_vehiculos/noimagen.svg',
        blank=True,
        null=True,
    )
    marca = models.CharField(max_length=200)
    modelo = models.CharField(max_length=200)
    categoria = models.CharField(max_length=3, choices=Category, default=Category.POLICIA)

    def __str__(self):
        return self.matricula
