# urls.py

from django.urls import path
from .views import custom_login_view,forget_password_view, user_signup_view, user_profile_view,edit_profile_view,user_logout_view,change_password_view,user_management_view,all_users_view,delete_user_view,edit_user_view,change_user_status_view,otp_input_view

urlpatterns = [
    
    path('login/', custom_login_view, name='login'),
    path('logout/', user_logout_view, name='logout'),
    path('signup/', user_signup_view, name='signup'),
    path("my-profile/", user_profile_view, name="myprofile"),
    path("edit-profile/", edit_profile_view, name="editprofile"),
    path("change-password/", change_password_view, name="change-password"),
    path('forgetpassword/', forget_password_view,name='forgetpassword'),
    path('all-users/', all_users_view, name='allusers'),
    path('user-management/', user_management_view, name='usermanagement'),
    path('edit-user/<int:pk>', edit_user_view, name="edit-user"),
    path('delete-user/<int:pk>/', delete_user_view, name="delete-user"),
    path("change-user-status/<int:pk>", change_user_status_view, name="change-user-status"),
    path("otp-input", otp_input_view, name="otpinput"),
]
