# urls.py

from django.urls import path
from .views import custom_login_view,forget_password_view

urlpatterns = [
    
    path('login/', custom_login_view, name='login'),
    path('forgetpassword', forget_password_view,name='forgetpassword'),
]
