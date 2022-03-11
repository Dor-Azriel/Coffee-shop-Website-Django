from django.shortcuts import render
from django.views.generic import CreateView, UpdateView, DeleteView
from .models import item,Menu,item_menu,payment
from django.forms import DateInput
from django import forms


class add_item(CreateView,  ):
    model = item
    fields = ['name', 'price', 'photo', 'special_price', 'strat_hour', 'end_hour', 'available', 'special']
    item.strat_hour = forms.DateField(widget=DateInput)
    def get_form_kwargs(self):
        kwargs = super(add_item, self).get_form_kwargs()
        print(kwargs)
        return kwargs

class add_payment(CreateView,  ):
    model = payment
    fields = ['full_name','credit_num','expiry_date','ccv',]
    payment.strat_hour = forms.DateField(widget=DateInput)

    def get_form_kwargs(self):
        kwargs = super(add_payment, self).get_form_kwargs()
        print(kwargs)
        return kwargs

class update_item(UpdateView,):
    model = item
    fields = ['name', 'price', 'photo', 'special_price', 'strat_hour', 'end_hour', 'available', 'special']


class delete_item(DeleteView,):
    model = item


class add_menu(CreateView,  ):
    model = Menu
    fields = ['name', 'strat_hour', 'end_hour',]
    item.strat_hour = forms.DateField(widget=DateInput)
    def get_form_kwargs(self):
        kwargs = super(add_menu, self).get_form_kwargs()
        print(kwargs)
        return kwargs


class update_menu(UpdateView,):
    model = Menu
    fields = ['name', 'strat_hour', 'end_hour',]


class delete_menu(DeleteView,):
    model = Menu

class add_item_menu(CreateView,  ):
    model =item_menu
    fields = ['item',]
    #item.strat_hour = forms.DateField(widget=DateInput)
    def get_form_kwargs(self):
        kwargs = super(add_item_menu, self).get_form_kwargs()
        print(kwargs)
        return kwargs