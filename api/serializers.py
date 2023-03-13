from rest_framework import serializers
from django.utils.translation import gettext as _
from .models import *

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
     
        
class ProfileDetailSerializer(serializers.ModelSerializer):
    
    email = serializers.EmailField(required=True)
    events=EventSerialier(many=True)
    socialmedia_link= SocialmediaSerializer(many=True)
    class Meta:
        model = User
        fields =(
             'email',
             'events',
             'timezone',
             'city',
             'address',
             "first_name",
             "last_name",
             "phone_number",
             "bio",
            "available_from",
            "available_to",
            "off_weekdays",
            "profile_image",
            "socialmedia_link"
            )
            
        
  
              
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
    
        
class UpdateUserSerializer(serializers.ModelSerializer):
    
    email = serializers.EmailField(min_length=8, required=True)
    socialmedia_link= SocialmediaSerializer(many=True)

    class Meta:
        model = User
        fields =["email","socialmedia_link"]
        
    def create(self,validated_data):
        
        socialmedia_link=validated_data.pop('socialmedia_link')
        # user=User.objects.create(**validated_data) 
        email=validated_data.get('email')
        user=User.objects.get(email=email)
        for social in socialmedia_link:
            Socialmedia.objects.create(**social,user=user)
        return user
    
     
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
        
