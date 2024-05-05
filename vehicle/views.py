from django.shortcuts import render, redirect, HttpResponse
from .forms import VehicleForm
from .models import VehicleImage, Vehicle
from django.core.paginator import Paginator
import uuid
from django.contrib import messages
from django.contrib.auth.decorators import login_required
import datetime
from datetime import timedelta
import json
import csv

def create_vehicle(request):
    print("in add view", request.FILES)
    vehicle = Vehicle.objects.create(plate_number="vehicledsdsd",contract_number="contract_ndsdsdsumber") 
    for key, uploaded_files in request.FILES.lists():
                # Create a VehicleImage instance for each uploaded image
                for uploaded_file in uploaded_files:
                    vehicle_image = VehicleImage(vehicle=vehicle)
                    vehicle_image.image_file.save(uploaded_file.name, uploaded_file)
                    vehicle_image.save()
                messages.success(request, "Vehicle added successfully")
   
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

@login_required
def archive_search_view(request):
  print("resuest post", request.POST)
  if request.method == 'POST':
        license_plate_or_contract_number = request.POST.get('license_plate_or_contract_number')
        date_time = request.POST.get('dateTime')
        start_date = request.POST.get('startDate')
        end_date = request.POST.get('endDate')
        search_results = Vehicle.objects.all()
        if license_plate_or_contract_number:
            search_results = search_results.filter(plate_number__iexact=license_plate_or_contract_number) | \
                             search_results.filter(contract_number__iexact=license_plate_or_contract_number)

        if date_time == 'Last 24 hours':
            search_results = search_results.filter(date_time__gte=datetime.datetime.now() - timedelta(days=1))
        elif date_time == 'Last 3 days':
            search_results = search_results.filter(date_time__gte=datetime.datetime.now() - timedelta(days=3))
        elif date_time == 'Last 7 days':
            search_results = search_results.filter(date_time__gte=datetime.datetime.now() - timedelta(days=7))
        elif date_time == 'Last 30 days':
            search_results = search_results.filter(date_time__gte=datetime.datetime.now() - timedelta(days=30))
        elif date_time == 'Custom' and start_date and end_date:
            search_results = search_results.filter(date_time__range=[start_date, end_date])

        return render(request, 'archive_search.html', {'search_results': search_results})
  return render(request, 'archive_search.html')


def export_result_view(request):
     if request.method == 'POST':
        data = json.loads(request.POST['data'])

        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="exported_data.csv"'

        writer = csv.DictWriter(response, fieldnames=data[0].keys())
        writer.writeheader()
        for row in data:
            writer.writerow(row)

        return response
     else:
        return HttpResponse('Method not allowed', status=405)