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

    # created = models.DateTimeField(auto_now_add=True)
    # updated = models.DateTimeField(auto_now=True)

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
        else:
            if not self.id:  # Solo si es un nuevo objeto
                self.created = timezone.now()
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
    # Cambio: quitar to_field="name" para que use el ID por defecto
    homeworld = models.ForeignKey(Planets, on_delete=models.CASCADE, db_column="homeworld", null=True)
    
    # created = models.DateTimeField(auto_now_add=True)
    # updated = models.DateTimeField(auto_now=True)
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
        else:
            if not self.id:  # Solo si es un nuevo objeto
                self.created = timezone.now()
            self.updated = timezone.now()
        super().save(*args, **kwargs)