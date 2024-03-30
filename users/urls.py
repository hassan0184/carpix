# urls.py

from django.urls import path
from .views import custom_login_view,forget_password_view, user_signup_view, user_profile_view,edit_profile_view,user_logout_view,change_password_view

urlpatterns = [
    
    path('login/', custom_login_view, name='login'),
    path('logout/', user_logout_view, name='logout'),
    path('signup/', user_signup_view, name='signup'),
    path("my-profile/", user_profile_view, name="myprofile"),
    path("edit-profile/", edit_profile_view, name="editprofile"),
    path("change-password/", change_password_view, name="change-password"),
    path('forgetpassword', forget_password_view,name='forgetpassword'),
]
