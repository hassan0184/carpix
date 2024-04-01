from django.urls import path
from .views import Dashboard_View

urlpatterns = [
    
    path('', Dashboard_View, name='dashboard'),
]