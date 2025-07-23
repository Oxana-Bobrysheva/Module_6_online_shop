from django.contrib.auth.models import AbstractUser
from django.db import models
from django.forms import CharField
from phonenumber_field.modelfields import PhoneNumberField


# Create your models here.
class User(AbstractUser):
   username =  None
   email = models.EmailField(unique=True, verbose_name="Email")
   avatar = models.ImageField(upload_to="images/avatar/", verbose_name="avatar", null=True, blank=True )
   phone_number = PhoneNumberField(verbose_name="Телефон", blank=True, null=True, help_text='Введите свой номер телефона в формате +71112223344')
   country = models.CharField(verbose_name="country", blank=True, null=True)

   USERNAME_FIELD = "email"
   REQUIRED_FIELDS = []

   class Meta:
      verbose_name = "Пользователь"
      verbose_name_plural = "Пользователи"

   def __str__(self):
      return self.email