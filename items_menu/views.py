from django.shortcuts import render
from django.views.generic import CreateView, UpdateView, DeleteView
from .models import item
from django.forms import DateInput
from django import forms
from django.contrib.auth.models import User
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.contrib import messages

class NewUserForm(UserCreationForm):
    email = forms.EmailField(required=True)
    fields = ['username', 'email', 'password', ]
    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2")

    def save(self, commit=True):
        user = super(NewUserForm, self).save(commit=False)
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
        return user

def register_request(request):
    if request.method == "POST":
        form = NewUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "Registration successful." )
            return redirect("main:homepage")
        messages.error(request, "Unsuccessful registration. Invalid information.")
    form = NewUserForm()
    return render (request=request, template_name="register.html", context={"register_form":form})


class add_item(CreateView,  ):
    model = item
    fields = ['name', 'strat_hour', 'end_hour']
    item.strat_hour = forms.DateField(widget=DateInput)
    def get_form_kwargs(self):
        kwargs = super(add_item, self).get_form_kwargs()
        print(kwargs)
        return kwargs
class update_item(UpdateView,):
    model = item
    fields = ['name', 'strat_hour', 'end_hour', ]

class delete_item(DeleteView,):
    model = item


def home_view(request,*args,**kargs):
    return render(request, "start.html")