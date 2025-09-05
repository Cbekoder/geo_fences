from django.db import models
from django.utils import timezone

class GeoFence(models.Model):
    name = models.CharField(max_length=100)
    center_lat = models.FloatField()
    center_lon = models.FloatField()
    radius_km = models.FloatField()

    def __str__(self):
        return self.name

class DeviceState(models.Model):
    device_id = models.CharField(max_length=100, unique=True)
    is_inside = models.CharField(max_length=10, choices=[("inside", "Inside"), ("outside", "Outside")])
    updated_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"{self.device_id}: {self.is_inside}"