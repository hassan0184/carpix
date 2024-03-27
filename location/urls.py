from django.urls import path
from .views import location_management,booth_management,camera_management

urlpatterns = [
    path('location-management/', location_management, name='location_management'),
    path('booth-management/', booth_management, name='booth_management'),
    path('camera-management/', camera_management, name='camera_management'),
]
