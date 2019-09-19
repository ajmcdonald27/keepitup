from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy, reverse
from django.views import generic
from keepitapp.models import User
from django.contrib.auth.views import LoginView
from django.urls import path
from django.http import HttpResponse
from keepitapp.views import TaskView
from django import forms
from django.forms import ModelForm
import pytz

class UserCreateForm(UserCreationForm):

    choices = []
    for tz in pytz.common_timezones:
        choices.append((tz,tz))
    timezone = forms.ChoiceField(choices=choices)

    times = []
    for i in range(0,24):
        times.append((i,str(i) + ".00"))
    reset_time = forms.ChoiceField(choices=times)

    class Meta:
        model = User
        fields = ["username", "password1", "password2", "timezone", "reset_time"]

    def save(self, commit=True):
        user = super(UserCreateForm, self).save(commit=False)
        user.timezone = self.cleaned_data["timezone"]
        user.reset_time = self.cleaned_data["reset_time"]
        if commit:
            user.save()
        return user


class SignUp(generic.CreateView):
    form_class = UserCreateForm
    success_url = reverse_lazy('login')
    template_name = 'signup.html'





