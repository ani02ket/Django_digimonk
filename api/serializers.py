from rest_framework import serializers
from django.utils.translation import gettext as _
from .models import User,BilingInfo,EventInterest



class EventSerialier(serializers.ModelSerializer):
    class Meta:
        model=EventInterest
        fields=("event_category","status")
  
        
class UserRegisterSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(min_length=8, required=True)
    event=EventSerialier(many=True,read_only=True)
    timezone=serializers.CharField(max_length=32)
    class Meta:
        model = User
        fields =('email','event','timezone')
       
    def create(self, validated_data):
        try:
            event_ids = []
            for events in self.initial_data['event']:
                if 'event_category' not in events:
                    raise serializers.ValidationError({'detail': 'key error'})
                event_ids.append(events['event_category'])
               
              
            if event_ids:
                new_event =User.objects.create(**validated_data)
                for event_id in event_ids:
                    new_event.event.add(event_id)
            new_event.save()
            return new_event
        except Exception as e:
            raise serializers.ValidationError({'detail2': e})
    
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
    