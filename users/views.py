from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from users.models import User
from .utils import generate_random_password
from django.core.mail import send_mail
from users.forms.signup_form import UserSignupForm
from users.forms.edit_profile_form import EditProfileForm
from users.forms.change_password_form import ChangePasswordForm
from users.models import Profile
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db import IntegrityError



def custom_logout_view(request):
    logout(request)
    return redirect('login') 

def custom_login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('userpassword')

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect("dashboard")
        else:
            messages.error(request, 'Invalid Email or Password ')
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
            send_mail(
                'Password Reset',
                f'Your new password is: {new_password}',
                'cvmaker750@gmail.com',
                [email],
                fail_silently=False,
            )
            return redirect('login') 
        except User.DoesNotExist:
            messages.error(request, 'Please Enter Your Registered Email')
            return render(request, 'forget_password.html')
    else:
      return render(request, "forget_password.html")
    

def user_signup_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('userpassword')
        email = request.POST.get('useremail')
        fullname = request.POST.get('fullname')

        if email and password:
            try: 
                user = User.objects.create(username=username, email=email, fullname=fullname)
                user.set_password(password)
                user.save()
                messages.success(request, 'Account created successfully! You can now log in.')
                return render(request, "landing.html")
            except IntegrityError as e:
                if 'username' in str(e):
                    messages.error(request, 'Username is already taken. Please choose a different one.')
                elif 'email' in str(e):
                    messages.error(request, 'Email is already registered. Please use a different one.')
                else:
                    messages.error(request, 'An error occurred during registration.')
                return render(request, 'signup.html')
        else:
            messages.error(request, 'Please fill in all required fields.')
            return render(request, 'signup.html')
    else:
        return render(request, 'signup.html')






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
            return redirect('myprofile')
    else:
        profile_form = EditProfileForm(instance=request.user.profile)
    return render(request, 'edit_profile.html', {'profile_form': profile_form})

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
            
            messages.success(request, 'Your password has been changed successfully.')
            return redirect('login')
    else:
        form = UserSignupForm()
    return render(request, 'change_password.html', {'form': form})
