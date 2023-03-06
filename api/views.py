from django.http import HttpResponse
from django.shortcuts import render
from .models import User
from .serializers import *
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from .emails import *
import uuid
from rest_framework_simplejwt.tokens import RefreshToken


class RegistrationView(APIView):

    def post(self,request):
        serializer = UserRegisterSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(status=status.HTTP_201_CREATED)

class GenerateOTP(APIView):
    def post(self,request):
        serializer = GenerateOTPSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        otp= send_otp_via_email(serializer.data['email'])
        return Response(status=status.HTTP_201_CREATED)

class VerifyOTP(APIView):
    def post(self,request):
        try:
            data=request.data
            serializer=VerifyAccountSerializer(data=data)
            if serializer.is_valid():
                email=serializer.data['email']
                otp=serializer.data['otp']
                
                user=User.objects.filter(email=email)                
                if not user.exists():
                    otp= send_otp_via_email(serializer.data['email'])
                    print(otp)
                    return Response(status=status.HTTP_404_NOT_FOUND)
                    
                if user[0].otp!=otp:
                    return Response({
                        'message':'Invalid OTP'
                    })
                
                user[0].save()
                
                
                return Response({'message':'Account is verified'})
        except Exception as e:
            print(e)
            
            
class Billing(APIView):
    def post(self,request):
        serializer = BillingInfoSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(status=status.HTTP_201_CREATED)
        

class UserLogin(APIView):
    def post(self,request): 
        email = self.request.data.get("email")
        password = self.request.data.get("password")
        user=User.objects.get(email=email)
        refresh = RefreshToken.for_user(user)
        if email and password:
            serializer = UserLoginSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            return Response({
                'refresh': str(refresh),
                'access': str(refresh.access_token),
                })
            
        else:
            serializer = UserLoginSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            email_token=send_email_token(serializer.data['email'],str(refresh.access_token))
            return Response({"message":f" please check mail to login  "})

def VerifyToken(request,token):
    try:
        obj=User.objects.get(email_token=token)
        return HttpResponse('Your account is verified you are logged in')  
    except Exception as e:
        return HttpResponse('Invalid token')

