from django.db import models

class Vehicle(models.Model):
    plate_number = models.CharField(max_length=20)
    contract_number = models.CharField(max_length=50)

    def __str__(self):
        return f"{self.plate_number} - {self.contract_number}"

class VehicleImage(models.Model):
    image_file = models.ImageField(upload_to='images/', blank=True,null=True)
    vehicle = models.ForeignKey(Vehicle, related_name="vehicle_images", on_delete=models.CASCADE)

    def __str__(self):
        return f"Image for {self.vehicle}"
