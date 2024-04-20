from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from django.shortcuts import render, redirect
from .models import Location,Booth,Camera
from django.contrib import messages
from django.http import StreamingHttpResponse, HttpResponse, HttpResponseServerError
import cv2,os
import numpy as np
import requests
from django.shortcuts import render, get_object_or_404


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


def view_booth_cameras(request, booth_id):
    booths=Booth.objects.all().order_by('-id')
    booth = get_object_or_404(Booth, pk=booth_id)
    cameras = booth.camera_set.all() 
    return render(request, 'view_booth_cameras.html', {'booth': booth,'booths': booths, 'cameras': cameras})

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
        ip_address=request.POST.get("ip_address")
        if camera_name and location_id and booth_id and ip_address:
            location = Location.objects.get(pk=location_id)
            booth = Booth.objects.get(pk=booth_id)
            Camera.objects.create(name=camera_name, location=location, booth=booth, ip_address=ip_address)
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

# def view_camera_feed(request):
#     cap = cv2.VideoCapture('http://196.12.185.250:20205/getimage?profileid=0')
#     def generate():
#         while True:
#             ret, frame = cap.read()
#             if not ret:
#                 break
#             ret, buffer = cv2.imencode('.jpg', frame)
#             if not ret:
#                 break
#             yield (b'--frame\r\n' b'Content-Type: image/jpeg\r\n\r\n' + buffer.tobytes() + b'\r\n')
#     return StreamingHttpResponse(generate(), content_type="multipart/x-mixed-replace;boundary=frame")


# views.py

def view_camera_feed(request, booth_id):
    booth = get_object_or_404(Booth, pk=booth_id)
    cameras = Camera.objects.filter(booth=booth, status='active')  
    return render(request, 'view_camera_feed.html', {'booth': booth, 'cameras': cameras})



def camera_stream_view(request):
  return render(request, 'stream_template.html')
