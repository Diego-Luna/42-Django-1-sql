from django.db import models
from django.utils import timezone

class Planets(models.Model):
    name = models.CharField(max_length=64, unique=True, null=False)
    climate = models.CharField(max_length=255, null=True)
    diameter = models.IntegerField(null=True)
    orbital_period = models.IntegerField(null=True)
    population = models.BigIntegerField(null=True)
    rotation_period = models.IntegerField(null=True)
    surface_water = models.FloatField(null=True)
    terrain = models.CharField(max_length=255, null=True)
    # Cambiamos auto_now_add y auto_now por default
    created = models.DateTimeField(default=timezone.now)
    updated = models.DateTimeField(default=timezone.now)
    
    def __str__(self):
        return self.name
    
    def save(self, *args, **kwargs):
        # Si es una carga directa (fixture), permitir valores explícitos
        if kwargs.get('raw', False):
            if hasattr(self, 'created') and self.created is None:
                self.created = timezone.now()
            if hasattr(self, 'updated') and self.updated is None:
                self.updated = timezone.now()
        super().save(*args, **kwargs)

class People(models.Model):
    name = models.CharField(max_length=64, null=False)
    birth_year = models.CharField(max_length=32, null=True)
    gender = models.CharField(max_length=32, null=True)
    eye_color = models.CharField(max_length=32, null=True)
    hair_color = models.CharField(max_length=32, null=True)
    height = models.IntegerField(null=True)
    mass = models.FloatField(null=True)
    homeworld = models.ForeignKey(Planets, on_delete=models.CASCADE, null=True)
    # Cambiamos auto_now_add y auto_now por default
    created = models.DateTimeField(default=timezone.now)
    updated = models.DateTimeField(default=timezone.now)
    
    def __str__(self):
        return self.name

class Movies(models.Model):
    title = models.CharField(max_length=64, unique=True, null=False)
    episode_nb = models.IntegerField(primary_key=True)
    opening_crawl = models.TextField(null=True)
    director = models.CharField(max_length=32, null=False)
    producer = models.CharField(max_length=128, null=False)
    release_date = models.DateField(null=False)
    # Cambiamos auto_now_add y auto_now por default
    created = models.DateTimeField(default=timezone.now)
    updated = models.DateTimeField(default=timezone.now)
    # Many-to-many relationship with People
    characters = models.ManyToManyField(People, related_name='movies')
    
    def __str__(self):
        return self.title