from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from django.shortcuts import render, redirect
from .models import Location

@staff_member_required
@login_required
def location_management(request):
    if request.method == 'POST':
        location_name = request.POST.get('name')
        if location_name:
            Location.objects.create(name=location_name)
            return redirect('location_management')

    locations = Location.objects.all()
    return render(request, 'location_management.html', {'locations': locations})


@staff_member_required
@login_required
def booth_management(request):
    pass


@staff_member_required
@login_required
def camera_management(request):
    pass
