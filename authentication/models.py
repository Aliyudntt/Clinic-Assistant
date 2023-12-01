from django.db import models
from django.core.exceptions import ValidationError
from django.core.exceptions import NON_FIELD_ERRORS


from django.contrib.auth.models import (
    BaseUserManager, AbstractBaseUser
)


BRANCH_CHOICES=[
    ('main campus', 'MAIN CAMPUS'),
    ('city campus', 'CITY CAMPUS'),
]


class AuthUserManager(BaseUserManager):
    use_in_migrations = True

    def _create_user(self, username, email, password, **extra_fields):
        if not email:
            raise ValueError('Email must be set')

        if not username:
            raise ValueError('Username must be set')
        email = self.normalize_email(email)
        user = self.model(username=username, email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user


    def create_user(self, username, email, password=None, **extra_fields):
        extra_fields.setdefault('is_admin',False)
        return self._create_user(username,email,password, **extra_fields)

    def create_superuser(self,username, email,password=None, **extra_fields):
        extra_fields.setdefault('is_admin', True)
        return self._create_user(username,email, password, **extra_fields)

        

class AuthUser(AbstractBaseUser):
    username = models.CharField(max_length=50, unique=True)
    email = models.EmailField(verbose_name="email address", max_length=255, unique=True)
    name = models.CharField(max_length=255)
    date_of_birth = models.DateField()
    contact_number = models.CharField(max_length=15)
    bmdc_reg_number = models.CharField(max_length=15)
    image = models.ImageField(max_length=500, upload_to="profileImages/", null=True, blank=True)
    about = models.TextField(default='', null=True,blank=True)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)

    objects = AuthUserManager()


    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email', 'date_of_birth', 'contact_number', 'bmdc_reg_number',]


    def get_full_name(self):
        return self.name

    
    def get_short_name(self):
        return self.username

    
    def __str__(self):
        return self.name

    
    def has_perm(self, perm, obj=None):
        return True 

    
    def has_module_perms(self, app_label):
        return True

    @property
    def is_staff(self):
        return self.is_admin
    
    
    def get_image(self):
        if self.image:
            return self.image.url
        return "/media/profileImages/noprofile.png"


    class Meta:
        verbose_name = "Dentist"
        verbose_name_plural="Dentists"


WEEK_DAYS = [
    ('All', "ALL"),
    ('Sunday', "SUNDAY"),
    ('Monday', "MONDAY"),
    ('Tuesday', "TUESDAY"),
    ('Wednesday', 'WEDNESDAY'),
    ('Thursday', "THURSDAY"),
    ('Friday', "FRIDAY"),
    ('Saturday', "SATURDAY"),
]


class Schedule(models.Model):
    dentist = models.ForeignKey(AuthUser, on_delete=models.CASCADE, related_name='schedule')
    start = models.TimeField()
    end = models.TimeField()
    branch_name = models.CharField(max_length=15, choices=BRANCH_CHOICES, default="uttara")
    weekday = models.CharField(choices=WEEK_DAYS, default="Sunday", max_length=10)
    max_patient = models.PositiveIntegerField(default=15)


    def validate_unique(self, *args, **kwargs):
          super(Schedule, self).validate_unique(*args, **kwargs)
          if self.start and self.end and self.start >= self.end:
              raise ValidationError({
            NON_FIELD_ERRORS: ["Schedule Start time cannot be greater than schedule end time"]
        })
    def __str__(self):
        return "%s %s %s-%s" %(self.dentist.name, self.weekday, str(self.start), str(self.end))

