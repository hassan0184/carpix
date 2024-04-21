from django.shortcuts import render
from location.models import Location,Booth,Camera
from vehicle.models import Vehicle
from users.models import User

def Dashboard_View(request):
    locations = Location.objects.all()
    booths = Booth.objects.all()  
    locations=Location.objects.all()
    vehicles=Vehicle.objects.all()
    users=User.objects.all()
    cameras=Camera.objects.all()
    return render(request, 'dashboard.html', {'locations': locations,'booths': booths, vehicles:vehicles, "users":users,"cameras":cameras})