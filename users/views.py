from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from users.models import User
from .utils import generate_random_password,send_password_reset_email
from users.forms.signup_form import UserSignupForm
from users.forms.edit_profile_form import EditProfileForm
from users.forms.change_password_form import ChangePasswordForm
from users.models import Profile
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db import IntegrityError
from users.utils import send_otp
from datetime import datetime
import pyotp
import threading




def custom_logout_view(request):
    del request.session['is_logged']
    del request.session["email"]
    del request.session["username"]
    logout(request)
    return redirect('login') 

def custom_login_view(request):
    if request.user.is_authenticated:
        return redirect("dashboard")
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('userpassword')

        user = authenticate(request, username=username, password=password)
        if user is not None:
            request.session["username"] = username
            request.session["email"] = user.email
            request.session['is_logged'] = True
            # Call send_otp function in the main thread to ensure session variables are set
            send_otp(request)
            return redirect("otpinput")
        else:
            messages.error(request, 'Invalid Username or Password')
            return render(request, 'login.html')
    else:
        return render(request, 'login.html')



def forget_password_view(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        try:
            user = User.objects.get(email=email)
            new_password = generate_random_password()
            user.set_password(new_password) 
            user.save()
            email_thread = threading.Thread(target=send_password_reset_email, args=(email, new_password))
            email_thread.start()

            messages.success(request, 'Password reset instructions sent to your email.')
            return redirect('login') 
        except User.DoesNotExist:
            messages.error(request, 'Please Enter Your Registered Email')
            return render(request, 'forget_password.html')
    else:
        return render(request, "forget_password.html")

    

def user_signup_view(request):

    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')
        fullname = request.POST.get('fullname')


        if User.objects.filter(username=username).exists():
            messages.error(request, 'User with the same username already exists')
            return redirect('signup') 

        if User.objects.filter(email=email).exists():
            messages.error(request, 'User with the same email already exists')
            return redirect('signup') 

        if len(password) < 8:
            messages.error(request, 'Password must be at least 8 characters long')
            return redirect('signup') 

        has_uppercase = any(char.isupper() for char in password)
        has_lowercase = any(char.islower() for char in password)
        has_numeric = any(char.isdigit() for char in password)
        
        if not (has_uppercase and has_lowercase and has_numeric):
            messages.error(request, 'Password must contain both uppercase and lowercase characters and at least one numeric digit')
            return redirect('signup') 

        if password != confirm_password:
            messages.error(request, 'Password and confirm password must match')
            return redirect('signup') 

        user = User.objects.create_superuser(
                fullname=fullname,
                email=email,
                username=username,
                password=password
            )
        Profile.objects.create(fullname=user.fullname,email=user.email, user=user)
        messages.success(request, "User successfully created")
        return redirect('signup')

    return render(request, 'signup.html', {'form': None})







@login_required 
def user_profile_view(request):
    if request.user:
        profile = Profile.objects.filter(user=request.user).first()
        return render(request, "user_profile.html", {"profile":profile})
    

@login_required
def edit_profile_view(request):
    if request.method == 'POST':
        profile_form = EditProfileForm(request.POST, instance=request.user.profile)
        if profile_form.is_valid():
            profile_form.save()
            messages.success(request, "Profile successfully edited")
            return redirect('myprofile')
        else:
            return render(request, 'edit_profile.html', {'profile_form': profile_form, "profile":request.user.profile, "errors":profile_form.non_field_errors})
    else:
        profile_form = EditProfileForm(instance=request.user.profile)

    return render(request, 'edit_profile.html', {'profile_form': profile_form, "profile":request.user.profile, "errors":profile_form.non_field_errors})

@login_required
def user_logout_view(request):
    logout(request)
    return render(request, "login.html")



@login_required
def change_password_view(request):
    if request.method == 'POST':
        form = ChangePasswordForm(request.POST)
        user = User.objects.filter(username=request.user.username).first()
        old_password = request.POST.get("old_password")
    
        if not user.check_password(old_password):
            messages.error(request, 'Old password is incorrect')
            return render(request, 'change_password.html', {'form': form})
        
        if form.is_valid():
            new_password = form.cleaned_data.get("new_password")
            user.set_password(new_password)
            user.save() 
            logout(request)
            messages.success(request, 'Your password has been changed successfully.')
            return redirect('login')
    else:
        form = UserSignupForm()
    return render(request, 'change_password.html', {'form': form})

@login_required
def user_management_view(request):
    if request.user.is_authenticated:
        if request.user.is_staff:
            if request.method == 'POST':
                form = UserSignupForm(request.POST)    
                if form.is_valid():
                    if request.POST.get("user_type").lower()=="simple_user":
                        user = User.objects.create_user(
                        fullname=form.cleaned_data.get("fullname"),
                        email=form.cleaned_data.get("email"),
                        username=form.cleaned_data.get("username"),
                        password=form.cleaned_data.get("password")
                    )
                    else:
                        user = User.objects.create_manager_user(
                            fullname=form.cleaned_data.get("fullname"),
                            email=form.cleaned_data.get("email"),
                            username=form.cleaned_data.get("username"),
                            password=form.cleaned_data.get("password")
                        )

                    Profile.objects.create(fullname=user.fullname,email=user.email, user=user)
                    messages.success(request, "User created successfully")
                    return render(request, "all_users.html", {"users":User.objects.all().exclude(role=1)})
            else:
                form = UserSignupForm()
            return render(request, 'user_management.html', {'form': form})
        else:
            return render(request, "permission_denied.html")
    messages.error(request, "Please login first")
    return redirect("login")



def all_users_view(request):
    if request.user.is_authenticated:
     return render(request, "all_users.html", {"users":User.objects.all().exclude(role=1)})
    messages.error(request, "please login first")
    return render(request,"login.html")

def delete_user_view(request, pk):
    if request.method == 'DELETE':
        users=User.objects.all().exclude(role=1).order_by('-id')
        if pk:
            User.objects.filter(id=pk).delete()
            messages.success(request, 'User Deleted Sucessfully')
            return render(request, 'all_users.html',{'users':users})
    return render(request, 'all_users.html',{'users':users})

@login_required
def edit_user_view(request, pk):
    if request.method == 'POST':
        user=User.objects.filter(id=pk).first()
        form = EditProfileForm(request.POST, instance=user.profile)
        if form.is_valid():
            form.save()
            messages.success(request, "User successfully updated")
            return redirect('allusers')
        else:
            return render(request, 'all_users.html', {'users': User.objects.all().exclude(role=1).order_by("-id"), "form":form})
    
    users=User.objects.all().exclude(role=1).order_by("-id")
    return render(request, 'all_users.html', {'users': users})

def change_user_status_view(request, pk):
    if request.user.is_authenticated:
        if request.user.is_staff:
            if request.method=="POST":
                user=User.objects.filter(id=pk).first()
                if request.POST.get("is_active")=="false":
                    user.is_active=False
                else:
                    user.is_active=True
                user.save()
                return redirect("allusers")
            return render(request, 'all_users.html', {'users': User.objects.all().exclude(role=1).order_by("-id")})
        else:
            return render(request, "permission_denied.html")
    messages.error(request, "please login first")
    return render(request,"login.html")


def otp_input_view(request):
    if request.user.is_authenticated:
        return redirect("dashboard")
    if request.method=="POST":
        username = request.session["username"]
        otp = request.POST.get('otp', '') 

        otp_secret_key = request.session["otp_secret_key"]
        otp_valid_date = request.session["otp_valid_date"]
        if otp_secret_key and otp_valid_date is not None:
            valid_untill = datetime.fromisoformat(otp_valid_date)
            if valid_untill > datetime.now():
                totp = pyotp.TOTP(otp_secret_key, interval=60)
                if totp.verify(otp):
                    login(request, User.objects.get(username=username))
                    del request.session["otp_secret_key"] 
                    del request.session["otp_valid_date"]
                    del request.session["username"]
                    return render(request, "dashboard.html") 
                else:
                    messages.error(request, "Invalid OTP entered")
            else:
                messages.error(request, "The OTP has expired")
                return redirect("otpinput")
        else:
            messages.error(request, "Something went wrong")

            return redirect("otpinput")
    return render(request, "otp.html")