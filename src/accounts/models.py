from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.utils.translation import gettext_lazy as _
from django.template.defaultfilters import slugify
        
from .managers import UserManager


class User(AbstractBaseUser, PermissionsMixin):
    full_name       = models.CharField(_('full name'), max_length=30)
    email           = models.EmailField(_('email address'), unique=True)
    is_staff        = models.BooleanField(_('staff status'), default=False)
    is_active       = models.BooleanField(_('active'), default=True)
    date_joined     = models.DateTimeField(_('date joined'), auto_now_add=True)
    is_applicant    = models.BooleanField(_('applicant'), default=False)
    is_employer     = models.BooleanField(_('employer'), default=False)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['full_name']

    class Meta:
        verbose_name = _('user')
        verbose_name_plural = _('users')
    
    def __str__(self): 
        return self.email

    def clean(self):
        super().clean()
        self.email = self.__class__.objects.normalize_email(self.email)


class Industry(models.Model):
    name = models.CharField(max_length=60)
    slug = models.SlugField(blank=True)

    class Meta:
        verbose_name_plural = "Industries"

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super(Industry, self).save(*args, **kwargs)


YEARS_OF_EXP = (
    ('entry', 'Entry Level'),
    ('1-2', '1-2 years'),
    ('3-5', '3-5 years'),
    ('6-10', '6-10 years'),
    ('above 10', 'Above 10 years')
)

GENDERS = (
    ('male', 'Male'),
    ('female', 'Female')
)

class Applicant(models.Model):
    user            = models.OneToOneField(User, on_delete=models.CASCADE)
    interest        = models.ForeignKey(Industry, on_delete=models.SET_NULL, blank=True, null=True)
    date_of_birth   = models.DateField(null=True, blank=True)
    location        = models.CharField(_('Where do you Reside now'), max_length=20, null=True, blank=True)
    gender          = models.CharField(max_length=10, choices=GENDERS, null=True, blank=True)
    about           = models.TextField(blank=True, null=True)
    years_of_exp    = models.CharField('Years of Experience', max_length=20, choices=YEARS_OF_EXP, null=True, blank=True)
    
    def __str__(self):
        return self.user.full_name



class Company(models.Model):
    user        = models.OneToOneField(User, on_delete=models.CASCADE)
    name        = models.CharField(_('company name'), max_length=50, null=True, blank=True)
    description = models.TextField(_('describe your company'), null=True, blank=True)
    website     = models.URLField(_('company webite'), null=True, blank=True)
    country     = models.CharField(max_length=40, null=True, blank=True)
    state       = models.CharField(max_length=40, null=True, blank=True)
    address     = models.CharField(_('company address'), max_length=120, null=True, blank=True)

    class Meta:
        verbose_name_plural = 'Companies'
    
    def __str__(self):
        return self.name
