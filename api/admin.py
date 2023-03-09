from django.contrib import admin
from .models import *

class UserAdmin(admin.ModelAdmin):
    list_display= ('email','password','otp','email_token')
      
admin.site.register(User,UserAdmin)
admin.site.register(EventInterest)
admin.site.register(WeekDays)
admin.site.register(EventDetails)
admin.site.register(ScheduledEvent)
admin.site.register(OpenSchedule)
admin.site.register(CombinedSchedule)



class BillingAdmin(admin.ModelAdmin):
    list_display= ('user','first_name','last_name','address','city','state_id','zip_code')
     
admin.site.register(BilingInfo,BillingAdmin)