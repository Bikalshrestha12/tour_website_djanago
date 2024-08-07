from typing import Any, Mapping
from django import forms
from django.contrib.auth.forms import UserChangeForm
from django.contrib.auth.models import User
from django.forms.renderers import BaseRenderer
from django.forms.utils import ErrorList
from publice.forms import *
from publice.models import *


class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)


class RegisterForm(forms.Form):
    username = forms.CharField()
    full_name = forms.CharField(max_length=150)
    email = forms.CharField(widget=forms.EmailInput)
    phone_no = forms.CharField(widget=forms.NumberInput)
    password = forms.CharField(widget=forms.PasswordInput)
    confirmation_password = forms.CharField(widget=forms.PasswordInput)


# class BookingForm(forms.Form):
#     class Meta:
#         model = Booking
#         field = "__all__"


class ContactForm(forms.Form):
    name = forms.CharField(max_length=100)
    email = forms.EmailField()
    subject = forms.CharField(max_length=200)
    message = forms.CharField(widget=forms.Textarea)


class InquireForm(forms.Form):
    class Meta:
        model = Inquire
        fields = "__all__"

        

class ProfileUpdateForm(UserChangeForm):
    class Meta:
        model = Profile
        fields = ["firstname","lastname","phone_number", "email_address", "address", "citizenship", "passport", "password"]

    def __init__(self, *args, **kwargs):
        super(ProfileUpdateForm, self).__init__(*args, **kwargs)
        self.fields.pop("password", None)

# class GalleryForm(forms.Form):
#     image = forms.ImageField()



class TourFilterForm(forms.Form):
    price = forms.MultipleChoiceField(
        choices=[('0-2000', '0 to 2000'), ('2000-10000', '2000 to 10000'), ('10000-above', '10000 and above')],
        required=False
    )
