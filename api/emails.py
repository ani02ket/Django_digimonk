from django.core.mail import send_mail
import random
from .models import User
from django.conf import settings
import uuid

def send_otp_via_email(email):
    subject='Your account verification email'
    otp=random.randint(1000,9999)
    message=f'Your otp is {otp}'
    email_from=settings.EMAIL_HOST_USER
    send_mail(subject,message,email_from,[email])
    user_obj=User.objects.get(email=email)
    user_obj.otp=otp
    user_obj.save()
    return user_obj.otp

def send_email_token(email,token):
    try:
        subject='Your account need to be verified'
        email_token=token
        message=f'Click here on the link to verify http://127.0.0.1:8000/VerifyToken/{email_token} '
        email_from=settings.EMAIL_HOST_USER
        send_mail(subject,message,email_from,[email])
        user_obj=User.objects.get(email=email)
        user_obj.email_token=email_token
        user_obj.save()
        return user_obj.email_token

    except Exception as e:
        return False
    
    return True
    
        

