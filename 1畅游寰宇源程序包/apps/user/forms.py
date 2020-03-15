__date__ = '2019/3/7 20:32'

from django import forms

from .models import UserProfile

class LoginForm(forms.Form):
    username=forms.CharField(required=True)
    password = forms.CharField(required=True)


class RegisterForm(forms.Form):
    username = forms.CharField(required=True)
    password1 = forms.CharField(required=True)
    password2 = forms.CharField(required=True)
