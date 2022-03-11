from django.core.validators import MaxValueValidator, MinValueValidator,URLValidator,RegexValidator
from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User
from django.db.models.signals import post_save, pre_save


class Menu(models.Model):
    name = models.CharField(null=False, max_length=300)
    strat_hour = models.CharField(null=True,validators=[RegexValidator(regex="^([0-1]?[0-9]|2[0-3]):[0-5][0-9]$"),]
                                ,max_length=5,blank=True)
    end_hour = models.CharField(null=True,validators=[RegexValidator(regex="^([0-1]?[0-9]|2[0-3]):[0-5][0-9]$"),]
                                ,max_length=5,blank=True)
    category = models.CharField(max_length=300, null=True,blank=True)
    location=[("out-side","out-side"),("in-side","in-side")]
    table_loc=models.CharField(max_length=20,choices=location,null=True)
    #price_range=models.
    def __str__(self):
        return self.name


class item (models.Model):
    name=models.CharField(null=False,max_length=300)
    price= models.FloatField(null=False,validators=[MinValueValidator(0)])
    photo=models.URLField(max_length=400,validators=[URLValidator],blank=True,null=True)
    special_price=models.FloatField(null=True,blank=True)
    strat_hour=models.CharField(null=True,validators=[RegexValidator(regex="^([0-1]?[0-9]|2[0-3]):[0-5][0-9]$"),]
                                ,max_length=5,blank=True)
    #end_hour = models.DateTimeField(null=True,blank=True)
    end_hour = models.CharField(null=True,validators=[RegexValidator(regex="^([0-1]?[0-9]|2[0-3]):[0-5][0-9]$"),]
                                ,max_length=5,blank=True)
    available = models.BooleanField(null=True,default=False)
    special = models.BooleanField(null=True,default=False)
    menu_key=models.ForeignKey(Menu,on_delete=models.CASCADE,null=True,blank=True)
    kinds=[("coffee","coffee"),("dish","dish"),("full-meal","full-meal"),("breakfast","breakfast"),("dinner","dinner"),("lunch","lunch"),
          ("alcohol","alcohol"),("beverage","beverage"),("business","business")]
    kind=models.CharField(max_length=20,choices=kinds)
    popularity= models.FloatField(default=0,validators=[MinValueValidator(0),MaxValueValidator(5)])
    is_vip = models.BooleanField(null=True,blank=True)
    vip_price=models.FloatField(null=True,blank=True,validators=[MinValueValidator(0)])
    desc = models.CharField(null=True,blank=True,max_length=600)
    def __str__(self):
        return self.name

class item_menu(models.Model):
    item=models.ForeignKey(item,on_delete=models.CASCADE)
    menu=models.ForeignKey(Menu,on_delete=models.CASCADE)

    def __str__(self):
        return "(" + str(self.item)+" , "+str(self.menu)+")"


class table(models.Model):
    number=models.IntegerField(null=False,validators=[MinValueValidator(0)])
    location=[("out-side","out-side"),("in-side","in-side")]
    loc=models.CharField(max_length=20,choices=location,null=True)
    active=models.BooleanField(default=False)
    reserve=models.BooleanField(default=False)

    def __str__(self):
        return "Table - " + str(self.number) +" "+ self.loc


class seat(models.Model):
    number=models.IntegerField(null=False,validators=[MinValueValidator(0)])
    table_key=models.ForeignKey(table,on_delete=models.CASCADE,null=True,blank=True)


class order(models.Model):
    time= models.DateTimeField(auto_now_add=True)
    table = models.ForeignKey(table,on_delete=models.CASCADE,null=True,blank=True)
    summary = models.FloatField(null=True,validators=[MinValueValidator(0)])
    payed =models.BooleanField(default=False)
    ready =models.BooleanField(default=False)

    def __str__(self):
        return "order number - "+str(self.pk)


class order_item(models.Model):
    item = models.ForeignKey(item,on_delete=models.CASCADE)
    order = models.ForeignKey(order,on_delete=models.CASCADE)
    started = models.BooleanField(default=False)
    def __str__(self):
        return "(" + str(self.item)+" , "+str(self.order)+")"


class table_room(models.Model):
    room_name =models.CharField(max_length=300,null=False)

class payment(models.Model):
    full_name=models.CharField(max_length=500, null=False)
    credit_number= models.IntegerField(null=True,validators=[MinValueValidator(0)])
    credit_num=models.CharField(null=False,max_length=300,validators=[RegexValidator("^(?:4[0-9]{12}(?:[0-9]{3})?|[25][1-7][0-9]{14}|6(?:011|5[0-9][0-9])[0-9]{12}|3[47][0-9]{13}|3(?:0[0-5]|[68][0-9])[0-9]{11}|(?:2131|1800|35\d{3})\d{11})$")])
    expiry_date=models.DateTimeField(null=False,)
    ccv=models.IntegerField(null=False,validators=[MinValueValidator(100),MaxValueValidator(999)])
    order = models.ForeignKey(order,on_delete=models.CASCADE,null=True)

    def get_absolute_url(self):
        return reverse("thanks_page")

def payment_hash(sender, instance,created, **kwargs):
    if created:
        payment.objects.filter(id=instance.id).update(credit_number=hash(instance.credit_number))

post_save.connect(payment_hash,sender=payment)