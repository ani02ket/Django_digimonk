from django.contrib import admin
from .models import User,BilingInfo

class UserAdmin(admin.ModelAdmin):
    list_display= ('email','password','otp','email_token','is_verified')
      
admin.site.register(User,UserAdmin)

class BillingAdmin(admin.ModelAdmin):
    list_display= ('user','first_name','last_name','address','city','state_id','zip_code')
     
admin.site.register(BilingInfo,BillingAdmin)