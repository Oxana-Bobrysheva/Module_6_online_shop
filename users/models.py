from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.forms import CharField
from phonenumber_field.modelfields import PhoneNumberField


class CustomUserManager(BaseUserManager):
   use_in_migrations = True

   def _create_user(self, email, password, **extra_fields):
      if not email:
         raise ValueError('Email must be set')
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

# Create your models here.
class User(AbstractUser):
   username =  None
   email = models.EmailField(unique=True, verbose_name="Email")
   avatar = models.ImageField(upload_to="images/avatar/", verbose_name="avatar", null=True, blank=True )
   phone_number = PhoneNumberField(verbose_name="Телефон", blank=True, null=True, help_text='Введите свой номер телефона в формате +71112223344')
   country = models.CharField(verbose_name="country", blank=True, null=True)

   USERNAME_FIELD = "email"
   REQUIRED_FIELDS = []

   objects = CustomUserManager()

   class Meta:
      verbose_name = "Пользователь"
      verbose_name_plural = "Пользователи"

   def __str__(self):
      return self.email