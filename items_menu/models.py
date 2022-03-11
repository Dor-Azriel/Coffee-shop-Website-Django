from django.core.validators import MaxValueValidator, MinValueValidator,URLValidator,RegexValidator
from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from django.core.exceptions import ValidationError
from django.contrib.auth.models import (
    BaseUserManager, AbstractBaseUser
)
class Menu(models.Model):
    name = models.CharField(null=False, max_length=300)
    strat_hour = models.DateTimeField(null=True)
    end_hour = models.DateTimeField(null=True)
    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('menu', kwargs={})

class item (models.Model):
    name=models.CharField(null=False,max_length=300)
    price= models.FloatField(null=False,validators=[MinValueValidator(0)])
    photo=models.URLField(max_length=400,validators=[URLValidator])
    special_price=models.FloatField(null=True,blank=True)
    strat_hour=models.DateTimeField(null=True,blank=True)
    end_hour = models.DateTimeField(null=True,blank=True)
    #end_hour = models.CharField(null=True,validators=[RegexValidator(regex="^([0-1]?[0-9]|2[0-3]):[0-5][0-9]$"),])
    available = models.BooleanField(null=True,default=False)
    special = models.BooleanField(null=True,default=False)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('item', kwargs={})

class item_menu(models.Model):
    item=models.ForeignKey(item,on_delete=models.CASCADE)
    menu=models.ForeignKey(Menu,on_delete=models.CASCADE)

class User(AbstractBaseUser):
    email = models.EmailField(
        verbose_name='email address',
        max_length=255,
        unique=True,
    )
    USERNAME_FIELD = 'email'
    is_vip=models.BooleanField()
    roles= [("Barista","Barista"),("client","client"),("manage","manage")]