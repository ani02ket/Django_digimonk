from django.urls import  path
from .views import *

from rest_framework_simplejwt import views as jwt_views





urlpatterns = [
    path("register/", RegistrationView.as_view(), name="register"),

    path("verify/",VerifyOTP.as_view()),
    path("otp/",GenerateOTP.as_view()),
    path("billing/",Billing.as_view()),
    path("UserLogin/",UserLogin.as_view()),
    path("VerifyToken/<token>",VerifyToken),
    path("event/",EventDetails.as_view()),   
    path("SocialMedia/",SocialMedia.as_view()),
    path("UserDetail/", UserDetail.as_view(), name="UserDetail"),
    path(
        "change-profile-details/",
        ChangeProfileDetailView.as_view(),
        name="change_profile_details",
    ),
    path('ChangeEmail/<id>',ChangeEmail.as_view())
]