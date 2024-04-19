from django.urls import path
from .views import add_location,view_location,delete_location,add_booth,view_booth,delete_booth,add_camera,view_camera,delete_camera,view_camera_feed,camera_stream_view

urlpatterns = [
    path('add-location/', add_location, name='add_location'),
    path('view-location/', view_location, name='view_location'),
    path('delete-location/<int:id>', delete_location, name='delete_location'),
    path('add-booth/', add_booth, name='add_booth'),
    path('view-booth/', view_booth, name='view_booth'),
    path('delete-booth/<int:id>', delete_booth, name='delete_booth'),
    path('add-camera/', add_camera, name='add_camera'),
    path('view-camera/', view_camera, name='view_camera'),
    path('view-camera-feed/', view_camera_feed, name='view_camera_feed'),
    path('delete-camera/<int:id>', delete_camera, name='delete_camera'),
    path("camera-stream-view/",camera_stream_view, name="camera-stream-view" )
]
