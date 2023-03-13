from rest_framework import serializers
from django.utils.translation import gettext as _
from .models import *

from rest_framework.exceptions import ValidationError

class WeekDaysSerializer(serializers.ModelSerializer):
    class Meta:
        model = WeekDays
        fields = "__all__"

# class AvailabilitySerializer(serializers.ModelSerializer):
#     user_availability_time_slot = AvailabilityTimeSlotsSerializer(many=True)

#     class Meta:
#         model = Availability
#         fields = (
#             "id",
#             "weekdays_id",
#             "specific_hours_date",
#             "user_availability_time_slot",
#         )



class EventSerialier(serializers.ModelSerializer):
    event_category = serializers.CharField(required=True)
    class Meta:
        model=EventInterest
        fields=("event_category","status")
  
class EventDetailsSerializer(serializers.ModelSerializer):
    event_name=serializers.CharField(max_length=50)
    
    class Meta:
        model=EventDetails
        fields = ("event_name","Description")
        
        
class SocialmediaSerializer(serializers.ModelSerializer):
    social_media_name=serializers.CharField(max_length=50)
    url=serializers.URLField()
    class Meta:
        model=Socialmedia
        fields=["user","social_media_name","url"]
        read_only_fields=("user",)
        
  
              
class UserRegisterSerializer(serializers.ModelSerializer):

    email = serializers.EmailField(min_length=8, required=True)
    # socialmedia_link= SocialmediaSerializer(many=True,read_only=True)

    class Meta:
        model = User
        fields =["email",]
        
    
    def validate_email(self, value):

        if(User.objects.filter(email__iexact=value).first()):
            raise serializers.ValidationError(_("This Email already exists."))

        return value
    
class ChangeProfileDetailSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(required=True)
    socialmedia_link= SocialmediaSerializer(many=True)
    # profile_image = Base64ImageField(
    #     max_length=None,
    #     use_url=True,
    #     required=False,
    #     allow_null=True,
    #     allow_empty_file=True,
    # )

    class Meta:
        model = User
        fields = [
            "email",
            # "username",
            "first_name",
            "last_name",
            # "user_type",
            "phone_number",
            "timezone",
            "bio",
            "available_from",
            "available_to",
            "socialmedia_link"
            # "off_weekdays",
            # "events"
            # "profile_image",
        ]

    def validate_email(self, value):
        self.email = value
        if not User.objects.filter(email__iexact=self.email).first():
            raise ValidationError(_("Email doesn't exists."))

        if not User.objects.filter(email__iexact=self.email, is_active=True).first():
            raise ValidationError(_("Email is not verified"))

        self.instance = User.objects.get(email__iexact=self.email)
        return value

    def save(self):
        
        email=self.validated_data.pop("email")
        user=User.objects.get(email=email)
        social_media=self.validated_data.pop('socialmedia_link')
        for social in social_media:
           Socialmedia.objects.create(**social,user=user)
        self.instance = self.update(self.instance, self.validated_data)
        return self.instance
       

    
     
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
    
class EventDetailsSerializer(serializers.ModelSerializer):
    event_name=serializers.CharField(max_length=50)
    
    class Meta:
        model=EventDetails
        fields = ("user","event_name","Description","course_link","Event_cost")
        
