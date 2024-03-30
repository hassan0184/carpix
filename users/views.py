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
            return render(request, "dashboard.html")
        else:
            return render(request, 'login.html', {'error': 'Invalid username or password'})
    else:
        return render(request, 'login.html')


def forget_password_view(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        try:
            user = User.objects.get(email=email)
            new_password = generate_random_password()
            user.set_password(new_password) 
            print("new password is :",new_password)
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
            return render(request, 'forget_password.html', {'error': 'User with this email does not exist'})
    else:
      return render(request, "forget_password.html")
    

def user_signup_view(request):
    if request.method == 'POST':
        form = UserSignupForm(request.POST)
        if form.is_valid():
            user = User.objects.create_superuser(
                email=form.cleaned_data.get("email"),
                username=form.cleaned_data.get("username"),
                password=form.cleaned_data.get("password")
            )
            profile = Profile.objects.create(
                first_name=form.cleaned_data.get("first_name", None),
                last_name=form.cleaned_data.get("last_name",None),
                email=form.cleaned_data.get("email"),
                user=user
            )
            messages.success(request, "Account created successfully")
            return redirect('login')
    else:
        form = UserSignupForm()
    return render(request, 'user_signup.html', {'form': form})

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

@login_required
def user_management_view(request):
    if request.method == 'POST':
        form = UserSignupForm(request.POST)    
        if form.is_valid():
            if request.POST.get("user_type").lower()=="simple_user":
                user = User.objects.create_user(
                    email=form.cleaned_data.get("email"),
                    username=form.cleaned_data.get("username"),
                    password=form.cleaned_data.get("password")
                )
            else:
                user = User.objects.create_manager_user(
                    email=form.cleaned_data.get("email"),
                    username=form.cleaned_data.get("username"),
                    password=form.cleaned_data.get("password")
                )

            profile = Profile.objects.create(
                first_name=form.cleaned_data.get("first_name", None),
                last_name=form.cleaned_data.get("last_name",None),
                email=form.cleaned_data.get("email"),
                user=user
            )
            messages.success(request, "User created successfully")
            return render(request, "all_users.html", {"users":User.objects.all().exclude(role=1)})
    else:
        form = UserSignupForm()
    return render(request, 'user_management.html', {'form': form})


def all_users_view(request):
    return render(request, "all_users.html", {"users":User.objects.all().exclude(role=1)})