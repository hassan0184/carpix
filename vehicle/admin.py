from django.contrib import admin

from .models import VehicleImage, Vehicle

admin.site.register(Vehicle)
admin.site.register(VehicleImage)