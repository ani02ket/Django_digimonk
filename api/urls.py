from django.urls import path
from .views import *
from rest_framework_simplejwt import views as jwt_views

urlpatterns = [
    path("register/", RegistrationView.as_view(), name="register"),
    path("verify/",VerifyOTP.as_view()),
    path("otp/",GenerateOTP.as_view()),
    path("billing/",Billing.as_view()),
    path("UserLogin/",UserLogin.as_view()),
    # path("VerifyToken/<token>", VerifyToken.as_view()),
    path("VerifyToken/<token>",VerifyToken)

]