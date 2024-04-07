from django.db import models
from simple_history.models import HistoricalRecords 

class Location(models.Model):
    name = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.name

class Booth(models.Model):
    location = models.ForeignKey(Location, on_delete=models.CASCADE)
    name = models.CharField(max_length=255, blank=True)

    def __str__(self):
        return f"{self.location.name} - Booth {self.id}" if self.name else f"{self.location.name} - Booth {self.id}"

class Camera(models.Model):
    location = models.ForeignKey(Location, on_delete=models.CASCADE)
    booth = models.ForeignKey(Booth, on_delete=models.CASCADE, blank=True, null=True)
    name = models.CharField(max_length=255, blank=True)
    status = models.CharField(max_length=20, choices=(('active', 'Active'), ('inactive', 'Inactive')), default='active')
    ip_address = models.CharField(max_length=255, blank=True, null=True)
    history = HistoricalRecords()


    def __str__(self):
        location_name = self.location.name
        booth_name = self.booth.name if self.booth else "General Area"
        return f"{location_name} - {booth_name} Camera - {self.name}"

