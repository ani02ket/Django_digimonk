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



    
class User(AbstractBaseUser, PermissionsMixin):

    """
    An abstract base class implementing a fully featured User model with
    admin-compliant permissions.

    Username and password are required. Other fields are optional.
    """
    # username_validator = UnicodeUsernameValidator()

    # username = models.CharField(
    #     _('username'),
    #     max_length=150,
    #     unique=True,
    #     help_text=_('Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.'),
    #     validators=[username_validator],
    #     error_messages={
    #         'unique': _("A user with that username already exists."),
    #     },blank=True
    # )
    first_name = models.CharField(_('first name'), max_length=150, blank=True)
    last_name = models.CharField(_('last name'), max_length=150, blank=True)
    email = models.EmailField(_('email address'), unique=True,  blank=True)
    otp=models.CharField(max_length=20,null=True,blank=True)
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
    # time_zone =
    available_from = models.TimeField(null=True, blank=True)
    available_to = models.TimeField(null=True, blank=True)
    off_weekdays = models.ManyToManyField(WeekDays)
    profile_image = models.ImageField(
        upload_to="Avatar", default=None, null=True, blank=True
    )

    objects = UserManager()
    USERNAME_FIELD = 'email'

    def __str__(self):
        return self.email

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
    

class BilingInfo(models.Model):
    user=models.OneToOneField(User,on_delete=models.CASCADE)
    card_number=models.BigIntegerField(null=True, blank=True)
    Exp_date= models.DateField(_("Exp_date"),default=timezone.now)
    cvv=models.CharField(max_length=3,null=True,default=None)
    card_zipcode=models.CharField(max_length=75, null=True, default=None)
    
    



    