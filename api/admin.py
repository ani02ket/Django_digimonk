from django.contrib import admin
from .models import User,BilingInfo

class UserAdmin(admin.ModelAdmin):
    list_display= ('email','password','otp')
      
admin.site.register(User,UserAdmin)

class BillingAdmin(admin.ModelAdmin):
    list_display= ('user','card_number','card_zipcode','Exp_date','cvv')
     
admin.site.register(BilingInfo,BillingAdmin)