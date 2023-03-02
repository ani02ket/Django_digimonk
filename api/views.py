from django.shortcuts import render
from .models import User
from .serializers import UserRegisterSerializer,GenerateOTPSerializer, VerifyAccountSerializer
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework import status
from rest_framework.exceptions import AuthenticationFailed
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken
from .emails import *
# Create your views here.

class RegistrationView(APIView):
    #permission_classes = [AllowAny]

    def post(self,request):
        serializer = UserRegisterSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({
            'status':200,
            'message':f"Successfully registered"
            
        })

class GenerateOTP(APIView):
    def post(self,request):
        serializer = GenerateOTPSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        otp= send_otp_via_email(serializer.data['email'])
        print(otp)
        
        return Response({
                        'status':400,
                        'message':f"Generated opt is {otp}"
                    })

class VerifyOTP(APIView):
    def post(self,request):
        try:
            data=request.data
            serializer=VerifyAccountSerializer(data=data)
            if serializer.is_valid():
                email=serializer.data['email']
                otp=serializer.data['otp']
                
                user=User.objects.filter(email=email)
                # print(user[0])
                
                if not user.exists():
                    otp= send_otp_via_email(serializer.data['email'])
                    print(otp)
                    return Response({
                        'status':400,
                        'message':'something went wronng',
                        'data':'Invalid email'
                    })
                    
                if user[0].otp!=otp:
                    return Response({
                        'status':400,
                        'message':'something went wronng',
                        'data':'Wrong otp'
                    })
                
                # user[0].is_verified=True
                user[0].save()
                
                
                return Response({
                    'status':200,
                    'message':'Account is verified',
                    'data': {}
                })
        except Exception as e:
            print(e)
            
            
# class LoginView(APIView):
#     def post(self,request):
#         try:
#             data=request.data
#             serializers=UserLoginSerializer(data=data)
#             if serializers.is_valid():
#                 email=serializers.data['email']
#                 password=serializers.data['password']
#                 print(email)
#                 print(password)
#                 user=authenticate(email =email ,password=password)
#                 print(user)
#                 if user is None:
#                     return Response({
#                         'status':400,
#                         'message':'invalid password',
#                         'data':{user}
                
#                         })
                    
#                 refresh=RefreshToken.for_user(user)
                
#                 return Response({
#                     'refresh':str(refresh),
#                     'access':str(refresh.access_token),
                    
#                 })
                    
#             return Response({
#                 'status':400,
#                 'message':'something went wrong'
        
                
#             })
            
#         except Exception as e:
#             print(e)
            
 
            
            
# class Updateview(APIView):
#     def patch(self,request,pk):
#         user_obj=User.objects.get(pk=pk)
#         data=request.data
#         serializer=UpdateSerializer(user_obj,data,partial=True)
        
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data)
        
#         else:
#             return Response(status=status.HTTP_404_NOT_FOUND)
