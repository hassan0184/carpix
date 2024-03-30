from django.shortcuts import render
from location.models import Location,Booth

def Dashboard_View(request):
    locations = Location.objects.all()
    booths = Booth.objects.all()  
    return render(request, 'home.html', {'locations': locations,'booths': booths})