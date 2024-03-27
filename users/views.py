from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from users.models import User
from .utils import generate_random_password
from django.core.mail import send_mail
from users.forms.signup_form import UserSignupForm

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
            return redirect('home') 
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
            print("in if")
            user = User.objects.create_superuser(
                email=form.cleaned_data.get("email"),
                username=form.cleaned_data.get("username"),
                password=form.cleaned_data.get("password")
            )
            print("created user", user)
            return redirect('login')
    else:
        print("in else")
        form = UserSignupForm()
    print("here", form.errors)
    return render(request, 'user_signup.html', {'form': form})