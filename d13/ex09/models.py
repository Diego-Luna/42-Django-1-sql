from django.db import models
from django.utils import timezone

# Create your models here.
class Planets(models.Model):
    names = models.CharField(max_length=64, null=False)
    climate = models.CharField(null=False)
    diameter = models.IntegerField(null=False)
    orbital_period = models.IntegerField(null=False)
    population = models.BigIntegerField(null=False)
    rotation_period = models.IntegerField(null=False)
    surface_water = models.FloatField(null=False)
    terrain = models.CharField(null=False)

    created = models.DateTimeField(default=timezone.now)
    updated = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.name

class People(models.Model):
    name = models.CharField(max_length=64, null=False)
    birth_year = models.CharField(max_length=32, null=False)
    gender = models.CharField(max_length=32, null=False)
    eye_color = models.CharField(max_length=32, null=False)
    hair_color = models.CharField(max_length=32, null=False)
    height = models.IntegerField(null=False)
    mass = models.FloatField(null=False)
    homeworld = models.ForeignKey(Planets, on_delete=models.CASCADE)

    created = models.DateTimeField(default=timezone.now)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name