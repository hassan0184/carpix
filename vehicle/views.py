from django.shortcuts import render, redirect
from .forms import VehicleForm
from .models import VehicleImage, Vehicle
from django.core.paginator import Paginator
import uuid
from django.contrib import messages


def create_vehicle(request):
    if request.method=="POST":
        form=VehicleForm(request.POST)
        if form.is_valid():
            vehicle = form.save()
            images = request.FILES.getlist("multiple_images")
            for image in images:
                VehicleImage.objects.create(vehicle=vehicle, image_file=image)
                messages.success(request, "Vehilce added sucessfully")
            return redirect("view-all-vehicles")
            
    return render(request, "add_vehicle.html", {"form":VehicleForm})

def view_all_vehicles(request):
    all_vehicles=Vehicle.objects.all().order_by("-id")
    paginator = Paginator(all_vehicles, 6)
    page_number = request.GET.get("page")
    vehicle_list = paginator.get_page(page_number)
    return render(request, "view_all_vehicles.html", {"vehicles":all_vehicles, "vehicle_list":vehicle_list})


def view_vehicle_detail(request, pk):
    vehicle=Vehicle.objects.filter(id=pk).first()
    return render(request, "vehicle_detail.html", {"vehicle":vehicle})

