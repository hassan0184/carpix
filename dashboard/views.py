from django.shortcuts import render
from location.models import Location

def Dashboard_View(request):
    locations = Location.objects.all()  
    return render(request, 'home.html', {'locations': locations})