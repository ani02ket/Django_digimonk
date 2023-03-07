from django.contrib import admin
from .models import User,BilingInfo,EventInterest,WeekDays

class UserAdmin(admin.ModelAdmin):
    list_display= ('email','password','otp','email_token')
      
admin.site.register(User,UserAdmin)
admin.site.register(EventInterest)
admin.site.register(WeekDays)
class BillingAdmin(admin.ModelAdmin):
    list_display= ('user','first_name','last_name','address','city','state_id','zip_code')
     
admin.site.register(BilingInfo,BillingAdmin)