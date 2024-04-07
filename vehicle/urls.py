
from django.urls import path
from .views import *
urlpatterns = [
    
    path("add/",create_vehicle, name="add-vehicle"),
    path("view/",view_all_vehicles, name="view-all-vehicles"),
    path("view/<int:pk>", view_vehicle_detail, name="vehicle-detail")
]
