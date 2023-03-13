from django.apps import apps
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import PermissionsMixin
from django.db import models
from django.template.defaultfilters import slugify
from django.utils.translation import gettext_lazy as _
from rest_framework_simplejwt.tokens import RefreshToken
from django.core.mail import send_mail
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.utils import timezone
import datetime
import pytz

TIMEZONES=tuple(zip(pytz.all_timezones,pytz.all_timezones))

class WeekDays(models.Model):
    day = models.CharField(_("Day"), max_length=50)
    slug_name = models.CharField(_("slug"), max_length=50)

    def __str__(self):
        return str(self.day)

    class Meta:
        verbose_name = _("Week Day")
        verbose_name_plural = _("Week Days")


# class UserType(models.Model):
#     user_type = models.CharField(_("Name"), max_length=50)
#     slug_name = models.CharField(_("slug"), max_length=50)

#     def __str__(self):
#         return str(self.user_type)

#     class Meta:
#         verbose_name = _("User Type")
#         verbose_name_plural = _("User Types")


class States(models.Model):
    state_name = models.CharField(max_length=50)
    status = models.BooleanField(default=True)

    def __str__(self):
        return str(self.state_name)

    class Meta:
        verbose_name = _("State")
        verbose_name_plural = _("States")


class UserManager(BaseUserManager):
    use_in_migrations = True

    def _create_user(self,email, password,user_type, **extra_fields):
        """
        Create and save a user with the given username, email, and password.
        """
        email = self.normalize_email(email)
        # Lookup the real model class from the global app registry so this
        # manager method can be used in migrations. This is fine because
        # managers are by definition working on the real model.
        user = self.model(email=email, **extra_fields)
        # if not  UserType.objects.filter(slug_name=slugify(user_type)).exists():
            #  user.user_type = UserType.objects.create(user_type="Admin",slug_name=slugify(user_type))
            
        # user.user_type = UserType.objects.get(slug_name=slugify(user_type))
        user.password = make_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email=None ,**extra_fields ):
        extra_fields.setdefault("is_staff", False)
        extra_fields.setdefault("is_superuser", False)
      
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.save(using=self._db)
        return user

    def create_superuser(
        self,email=None, password=None, user_type=None, **extra_fields
    ):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        user_type = "Admin"
        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")

        return self._create_user(email, password, user_type, **extra_fields)
    

    

class EventInterest(models.Model):
    
     event_category = models.CharField(max_length=50)
     status = models.BooleanField(default=False)

     def __str__(self):
        return str(self.event_category)
    


class ScheduledEvent(models.Model):
    sid=models.AutoField(primary_key=True)
    event_start=models.DateTimeField(_('event_start'), default=timezone.now)
    event_end= models.DateTimeField(_('event_end'), default=timezone.now)
    
    def __str__(self):
        return str(self.event_start)

class OpenSchedule(models.Model):
    timezone=models.CharField(max_length=32,choices=TIMEZONES,default='UTC')
    
    def __str__(self):
        return str(self.timezone)
    
class CombinedSchedule(ScheduledEvent,OpenSchedule):
        
    def __str__(self):
        return str(self.timezone)
    
  
class User(AbstractBaseUser, PermissionsMixin):

    """
    An abstract base class implementing a fully featured User model with
    admin-compliant permissions.

    Username and password are required. Other fields are optional.
    """
    # username_validator = UnicodeUsernameValidator()

    # username = models.CharField(
    #     _("username"),
    #     max_length=150,
    #     help_text=_(
    #         "Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only."
    #     ),
    #     validators=[username_validator],
    #     error_messages={
    #         "unique": _("A user with that username already exists."),
    #     },
    #     blank=True,
    # )
    first_name = models.CharField(_('first name'), max_length=150, blank=True)
    last_name = models.CharField(_('last name'), max_length=150, blank=True)
    email = models.EmailField(_('email address'), unique=True,  blank=True)
    otp=models.CharField(max_length=20,null=True,blank=True)
    email_token=models.CharField(max_length=200)
    is_verified=models.BooleanField(default=False)
    is_staff = models.BooleanField(
        _('staff status'),
        default=False,
        help_text=_('Designates whether the user can log into this admin site.'),
    )
    is_active = models.BooleanField(
        _('active'),
        default=True,
        help_text=_(
            'Designates whether this user should be treated as active. '
            'Unselect this instead of deleting accounts.'
        ),
    )
    date_joined = models.DateTimeField(_('date joined'), default=timezone.now)

    # user_type = models.ForeignKey(
    #     "UserType", verbose_name=_("User Type"), on_delete=models.CASCADE
    #   )
    phone_number = models.BigIntegerField(True, null=True, blank=True)
    timezone=models.CharField(max_length=32,choices=TIMEZONES,default='UTC')
    
    address = models.TextField(null=True, blank=True)
    city = models.CharField(max_length=75, default=None, null=True, blank=True)
    state_id = models.ForeignKey(
        States,
        verbose_name=_("User State"),
        on_delete=models.CASCADE,
        null=True,
        blank=True,
    )
   
    zip_code = models.CharField(max_length=75, default=None, null=True, blank=True)
    bio = models.TextField(null=True, blank=True)
    available_from = models.TimeField(null=True, blank=True)
    available_to = models.TimeField(null=True, blank=True)
    off_weekdays = models.ManyToManyField(WeekDays)
    events= models.ManyToManyField(EventInterest)
    
    profile_image = models.ImageField(
        upload_to="Avatar", default=None, null=True, blank=True
    )
    
    objects = UserManager()
    USERNAME_FIELD = 'email'

    def __str__(self):
        return self.email
    
    # @property
    # def choices(self):
    #     return self.choice_set.all()
    
    objects = UserManager()
    
    
    def clean(self):
        super().clean()
        self.email = self.__class__.objects.normalize_email(self.email)

    def get_full_name(self):
        """
        Return the first_name plus the last_name, with a space in between.
        """
        full_name = '%s %s' % (self.first_name, self.last_name)
        return full_name.strip()

    def get_short_name(self):
        """Return the short name for the user."""
        return self.first_name

    def email_user(self, subject, message, from_email=None, **kwargs):
        """Send an email to this user."""
        send_mail(subject, message, from_email, [self.email], **kwargs)

    def tokens(self): 
        refresh = RefreshToken.for_user(self)
        return {"refresh": str(refresh), "access": str(refresh.access_token)}
    
   
    
    
class Socialmedia(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE,related_name="socialmedia_link")
    social_media_name=models.CharField(max_length=50)
    url=models.URLField()

class BilingInfo(models.Model):
    user=models.OneToOneField(User,on_delete=models.CASCADE)
    first_name = models.CharField(_('first name'), max_length=150, blank=True)
    last_name = models.CharField(_('last name'), max_length=150, blank=True)
    address = models.TextField(null=True, blank=True)
    city = models.CharField(max_length=75, default=None, null=True, blank=True)
    state_id = models.ForeignKey(
        States,
        verbose_name=_("User State"),
        on_delete=models.CASCADE,
        null=True,
        blank=True,
    )
    zip_code = models.CharField(max_length=75, default=None, null=True, blank=True)
    

class EventDetails(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    event_name=models.CharField(_('event_name'), max_length=150)
    course_category= models.ManyToManyField(EventInterest)
    Description=models.TextField(max_length=200)
    location=models.CharField(max_length=75)
    course_link=models.URLField(max_length=200,unique=True)
    private_event=models.BooleanField(default=False,null=True)
    max_spots=models.IntegerField(blank=True, null=True)
    Event_cost=models.DecimalField(max_digits=10,null=True, decimal_places=2)
    transaction_fee=models.BooleanField(default=False,null=True)
    add_salestax=models.BooleanField(default=False,null=True)
    sales_tax=models.DecimalField(max_digits=10,null=True, decimal_places=2)

    def __str__(self):
        return str(self.event_name)

    
    
# class EventSchedule(models.Model):
#     scheduled_event=models.OneToOneField(ScheduledEvent,on_delete=models.CASCADE)
#     open_schedule=models.OneToOneField(OpenSchedule,on_delete=models.CASCADE) 
#     combined_schedule=models.OneToOneField(CombinedSchedule,on_delete=models.CASCADE)   
    
class DateModelMixin(models.Model):
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, null=True)

    class Meta:
        abstract = True    
    
      
class Availability(DateModelMixin):
    user_id = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="user_availability"
    )
    weekdays_id = models.ForeignKey(
        WeekDays,
        on_delete=models.SET_NULL,
        null=True,
    )
    
    def __str__(self):
        return f"USER ID:- {self.user_id} , WEEKDAYSS IDD:- {self.weekdays_id}"

    class Meta:
        verbose_name = _("Availability")
        verbose_name_plural = _("Availability")
        
        
class AvailabilityTimeSlots(DateModelMixin):
    availability_id = models.ForeignKey(
        Availability,
        on_delete=models.CASCADE,
        related_name="user_availability_time_slot",
    )
    from_time = models.TimeField()
    to_time = models.TimeField()

    class Meta:
        verbose_name = _("Availability")
        verbose_name_plural = _("Availability")