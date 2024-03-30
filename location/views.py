from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from django.shortcuts import render, redirect
from .models import Location,Booth
from django.contrib import messages

@staff_member_required
@login_required
def location_management(request):
    if request.method == 'POST':
        location_name = request.POST.get('location_name')
        if location_name:
            Location.objects.create(name=location_name)
            messages.success(request, 'Location Added Sucessfully')
            return redirect('home')

    locations = Location.objects.all()
    return render(request, 'location_management.html', {'locations': locations})


@staff_member_required
@login_required
def booth_management(request): 
    if request.method == 'POST':
        booth_name = request.POST.get('booth_name')
        booth_location_id = request.POST.get('booth_location')  # Get location id from the form
        if booth_name and booth_location_id:
            booth_location = Location.objects.get(pk=booth_location_id)  # Get the Location object using the id
            Booth.objects.create(name=booth_name, location=booth_location)
            messages.success(request, 'Booth Added Successfully')
            return redirect('home')
    booths=Booth.objects.all()
    return render(request, 'booth_management.html',{'booths':booths})


@staff_member_required
@login_required
def camera_management(request):
    pass
