from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.utils.translation import gettext_lazy as _


class UserManager(BaseUserManager):
    use_in_migrations = True

    def _create_user(self, email, password, **extra_fields):
        if not email:
            raise ValueError('The given email must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(email, password, **extra_fields)
        

class User(AbstractBaseUser, PermissionsMixin):
    full_name   = models.CharField(_('full name'), max_length=30)
    email       = models.EmailField(_('email address'), unique=True)
    is_staff    = models.BooleanField(_('staff status'), default=False)
    is_active   = models.BooleanField(_('active'), default=True)
    date_joined = models.DateTimeField(_('date joined'), auto_now_add=True)

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


class Applicant(models.Model):
    user            = models.OneToOneField(User, on_delete=models.CASCADE)
    date_of_birth   = models.DateField()
    location        = models.CharField(_('Where do you Reside now'), max_length=20)
    gender          = models.CharField(max_length=1)
    about           = models.TextField(blank=True, null=True)
    years_of_exp    = models.PositiveIntegerField(_('Years of Experience'))

    def __str__(self):
        return self.user


class Company(models.Model):
    name   = models.CharField(_('company name'), max_length=50)
    description = models.TextField(_('describe your company'))
    website     = models.URLField(_('company webite'))
    country     = models.CharField(max_length=40)
    state       = models.CharField(max_length=40)
    address     = models.CharField(_('company address'), max_length=120)

    def __str__(self):
        return self.name
