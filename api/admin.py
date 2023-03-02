from django.contrib import admin
from .models import User,BilingInfo

class UserAdmin(admin.ModelAdmin):
    list_display= ('email','password','otp')
      
admin.site.register(User,UserAdmin)

class BillingAdmin(admin.ModelAdmin):
    list_display= ('first_name','last_name','street_address','city','Exp_date','state','zip_code','cred_zipcode','cvv','phone_number')
     
admin.site.register(BilingInfo,BillingAdmin)