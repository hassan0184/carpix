import random
import string
import pyotp
import threading
from datetime import datetime, timedelta
from django.core.mail import send_mail

def generate_random_password(length=5):
    characters = string.ascii_letters + string.digits
    return ''.join(random.choice(characters) for _ in range(length))



def send_otp(request):
    totp=pyotp.TOTP(pyotp.random_base32(), interval=60)
    otp=totp.now()
    request.session["otp_secret_key"]=totp.secret
    valid_date=datetime.now() + timedelta(minutes=1)
    request.session["otp_valid_date"]=str(valid_date)
    print("your otp is", otp)
    send_mail(
                'OTP',
                f'Your OTP is: {otp}',
                'cvmaker750@gmail.com',
            [request.session["email"]],
                fail_silently=False,
            )

    
def send_password_reset_email(email, new_password):
    send_mail(
        'Password Reset',
        f'Your new password is: {new_password}',
        'cvmaker750@gmail.com',
        [email],
        fail_silently=False,
    )