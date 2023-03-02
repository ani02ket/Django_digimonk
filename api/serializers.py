from typing import Dict
from django.contrib.auth import get_user_model
from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from django.utils.translation import gettext as _
from rest_framework_simplejwt.tokens import RefreshToken
from .models import User,BilingInfo


class UserRegisterSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(min_length=8, required=True)
  #  password = serializers.CharField(min_length=6)

    class Meta:
        model = User
        fields =('email','otp')

    # def validate_username(self, value):
    #     if(len(value) > 10):
    #         raise serializers.ValidationError(_("username should be less than 10 Characters"))


    #     if(User.objects.filter(username__iexact=value).first()):
    #         raise serializers.ValidationError(_("Username already exists."))

    #     return value

    def validate_email(self, value):

        if(User.objects.filter(email__iexact=value).first()):
            raise serializers.ValidationError(_("This Email already exists."))

        return value

    # def create(self, validated_data:dict):   
    #     user = User.objects.create_user(email=validated_data['email'])
    #     # user.set_password(validated_data['password'])
    #     user.save()
    #     return user
    
class GenerateOTPSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(min_length=8, required=True)
    # otp=serializers.CharField(required=True)

    class Meta:
        model = User
        fields =('email','otp')
    
class VerifyAccountSerializer(serializers.Serializer):
    email=serializers.EmailField(min_length=8,required=True)
    otp=serializers.CharField(required=True)
    
    
    def validate_email(self, value):
        
        if(not User.objects.filter(email__iexact=value).first()):
            
            raise serializers.ValidationError(_("Email doesn't exist."))
        return value
           
class UserLoginSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(required=True)
    password=serializers.CharField(min_length=6)

    class Meta:
        model = User
        fields = ("email","password")

    def validate_email(self, value):
        
        if(not User.objects.filter(email__iexact=value).first()):
            
            raise serializers.ValidationError(_("Email doesn't exist."))
        return value
    
class UpdateSerializer(serializers.ModelSerializer):
    email = serializers.CharField(min_length=3, required=True)
    password = serializers.CharField(min_length=6)

    class Meta:
        model = User
        fields = ("username", "email", "password")


class BillingInfoSerializer(serializers.ModelSerializer):
  class Meta:
    model=BilingInfo
    fields = '__all__'