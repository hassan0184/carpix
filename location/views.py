from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from django.shortcuts import render, redirect
from .models import Location,Booth,Camera
from django.contrib import messages


def add_location(request):
    
    if request.method == 'POST':
        location_name = request.POST.get('location_name')
        if location_name:
            Location.objects.create(name=location_name)
            messages.success(request, 'Location Added Sucessfully')
            return redirect('add_location')

    return render(request, 'add_location.html')

def view_location(request):

    locations=Location.objects.all().order_by('-id')
    return render(request, 'view_location.html',{'locations':locations})


def delete_location(request,id):
    
    if request.method == 'DELETE':
        locations=Location.objects.all().order_by('-id')
        if id:
            Location.objects.filter(id=id).delete()
            messages.success(request, 'Location Deleted Sucessfully')
            return render(request, 'view_location.html',{'locations':locations})
    return render(request, 'view_location.html',{'locations':locations})



def add_booth(request):
    
    if request.method == 'POST':
        booth_name = request.POST.get('booth_name')
        booth_location_id = request.POST.get('booth_location')  
        if booth_name and booth_location_id:
            booth_location = Location.objects.get(pk=booth_location_id) 
            Booth.objects.create(name=booth_name, location=booth_location)
            messages.success(request, 'Booth Added Successfully')
            return redirect('add_booth')
    
    locations=Location.objects.all().order_by('-id')
    return render(request, 'add_booth.html',{"locations":locations})

def view_booth(request):

    booths=Booth.objects.all().order_by('-id')
    locations=Location.objects.all().order_by('-id')
    cameras=Camera.objects.all().order_by('-id')
    return render(request, 'view_booth.html',{'booths':booths,"locations":locations,"cameras":cameras})


def delete_booth(request,id):

    booths=Booth.objects.all().order_by('-id')
    if request.method == 'DELETE':
        if id:
            Booth.objects.filter(id=id).delete()
            messages.success(request, 'Booth Deleted Sucessfully')
            return render(request, 'view_booth.html',{'Booths':booths})
    return render(request, 'view_booth.html',{'booths':booths})



def add_camera(request):
    
    if request.method == 'POST':
        camera_name = request.POST.get('camera_name')
        location_id = request.POST.get('location') 
        booth_id = request.POST.get('booth')
        if camera_name and location_id and booth_id:
            location = Location.objects.get(pk=location_id)
            booth = Booth.objects.get(pk=booth_id)
            Camera.objects.create(name=camera_name, location=location, booth=booth)
            messages.success(request, 'Camera Added Successfully')
            return redirect('add_camera')
    
    booths=Booth.objects.all().order_by('-id')
    locations=Location.objects.all().order_by('-id')
    return render(request, 'add_camera.html',{'booths':booths,"locations":locations})

def view_camera(request):

    cameras=Camera.objects.all().order_by('-id')
    return render(request, 'view_camera.html',{'cameras':cameras})


def delete_camera(request,id):
    
    if request.method == 'DELETE':
        cameras=Camera.objects.all().order_by('-id')
        if id:
            Camera.objects.filter(id=id).delete()
            messages.success(request, 'Camera Deleted Sucessfully')
            return render(request, 'view_camera.html',{'cameras':cameras})
    return render(request, 'view_camera.html',{'cameras':cameras})


