from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from django.shortcuts import render, redirect
from .models import Location,Booth,Camera
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
        booth_location_id = request.POST.get('booth_location')  
        if booth_name and booth_location_id:
            booth_location = Location.objects.get(pk=booth_location_id) 
            Booth.objects.create(name=booth_name, location=booth_location)
            messages.success(request, 'Booth Added Successfully')
            return redirect('home')
    booths=Booth.objects.all()
    return render(request, 'booth_management.html',{'booths':booths})


@staff_member_required
@login_required
def camera_management(request):
    if request.method == 'POST':
        camera_name = request.POST.get('camera_name')
        location_id = request.POST.get('location') 
        booth_id = request.POST.get('booth')
        
        if camera_name and location_id and booth_id:
            location = Location.objects.get(pk=location_id)
            booth = Booth.objects.get(pk=booth_id)
            
            Camera.objects.create(name=camera_name, location=location, booth=booth)
            
            messages.success(request, 'Camera Added Successfully')
            return redirect('home')
    
    cameras = Camera.objects.all()
    return render(request, 'camera_management.html', {'cameras': cameras})

