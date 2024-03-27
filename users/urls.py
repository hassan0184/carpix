# urls.py

from django.urls import path
from .views import custom_login_view,forget_password_view, user_signup_view

urlpatterns = [
    
    path('login/', custom_login_view, name='login'),
    path('signup/', user_signup_view, name='signup'),
    path('forgetpassword', forget_password_view,name='forgetpassword'),
]
