from django.db import models
from django.contrib.auth.models import AbstractUser
from captcha.fields import CaptchaField
from django import forms
# Create your models here.


class UserProfile(AbstractUser):
    nick_name = models.CharField(max_length=50,verbose_name='昵称',default='',blank=True,null=True)
    class Meta:
        verbose_name="用户信息"
        verbose_name_plural=verbose_name

    def __str__(self):
        return self.username

class captcha_Form(forms.Form):
    captcha = CaptchaField()


