
from django.urls import path
from .views import *
urlpatterns = [
    
    path("add/",create_vehicle, name="add-vehicle"),
    path("view/",view_all_vehicles, name="view-all-vehicles"),
    path("view/<int:pk>", view_vehicle_detail, name="vehicle-detail"),
    path("archive-search/", archive_search_view, name="archive-search"),
    path("export-results/", export_result_view, name="export-results"),
]
