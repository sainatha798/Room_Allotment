__author__ = 'sainatha798'
from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Studentinfo

class Signup(UserCreationForm):
    first_name = forms.CharField(max_length=50,label='Name')
    username = forms.EmailField(required=True,max_length=50,label='Email')
    email = forms.EmailField(required=True,show_hidden_initial=True)
    password1 = forms.CharField(widget=forms.PasswordInput, label='Password')
    password2 = forms.CharField(widget=forms.PasswordInput, label='Confirm Password')

    ##confirm_password = forms.CharField(widget=forms.PasswordInput)
    class Meta:
        model = User
        fields = ['username','password1','password2','email']