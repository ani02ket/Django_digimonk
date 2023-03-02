from django.urls import path
from .views import RegistrationView,VerifyOTP,GenerateOTP
from rest_framework_simplejwt import views as jwt_views

urlpatterns = [
    path("register/", RegistrationView.as_view(), name="register"),
    path("verify/",VerifyOTP.as_view()),
    path("otp/",GenerateOTP.as_view()),
    # path("login/", LoginView.as_view(), name="login"),
    # path('gettoken/', jwt_views.TokenObtainPairView.as_view(), name='token_obtain_pair'),
    # path('refreshtoken/refresh/', jwt_views.TokenRefreshView.as_view(), name='token_refresh'),
    # path("update/<str:pk>",Updateview.as_view(),name="update"),
]