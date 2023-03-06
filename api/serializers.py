from rest_framework import serializers
from django.utils.translation import gettext as _
from .models import User,BilingInfo


class UserRegisterSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(min_length=8, required=True)

    class Meta:
        model = User
        fields =('email',)

    def validate_email(self, value):

        if(User.objects.filter(email__iexact=value).first()):
            raise serializers.ValidationError(_("This Email already exists."))

        return value

    
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
    password = serializers.CharField(required=False)


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
    fields = ("user","first_name","last_name","address","city","state_id","zip_code")
    