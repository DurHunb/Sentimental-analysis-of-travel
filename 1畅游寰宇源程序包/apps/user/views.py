from django.shortcuts import render
# 用户登录类型验证
import json
from django.contrib.auth import authenticate, login,logout
from django.contrib.auth.backends import ModelBackend
from django.views.generic.base import View
from django.http import HttpResponse,HttpResponseRedirect #重定向
# 利用django.core.urlresolvers.reverse 实现 index页面反转，通过url将index页面跳转给用户。
from  django.urls import reverse

from django.contrib import messages

# 密码加密
from django.contrib.auth.hashers import make_password
# 分页导入包
# Create your views here.
from .forms import LoginForm,RegisterForm
from .models import UserProfile,captcha_Form

class IndexView(View):
    def get(self, request):
        return render(request, "index.html", {})



class LoginView(View):
    # 登录
    def get(self, request):
        return render(request, "login.html", {})

    def post(self, request):
        login_form = LoginForm(request.POST)
        if login_form.is_valid():
            user_name = request.POST.get("username", '')
            pass_word = request.POST.get("password", '')
            user = authenticate(username=user_name, password=pass_word)
            if user is not None:
                login(request, user)
                from django.urls import reverse
                return HttpResponseRedirect(reverse("index"))
            else:
                return render(request, "login.html", {'msg': '用户名或密码错误！', 'login_form': login_form})
        else:
            return render(request, "login.html", {'login_form': login_form})


class RegisterView(View):
    # 注册
    def get(self, request):
        captcha_form = captcha_Form()
        return render(request, "register.html",{'captcha_form':captcha_form})

    def post(self, request):
        captcha_form = captcha_Form()
        reg = captcha_Form(request.POST)
        register_form = RegisterForm(request.POST)

        if reg.is_valid():
            if register_form.is_valid():

                user_name = request.POST.get("username", '')
                if UserProfile.objects.filter(username=user_name):
                    return render(request, "register.html", {'msg': '该用户已经存在','captcha_form':captcha_form})
                password1 = request.POST.get("password1", '')
                password2 = request.POST.get("password2", '')
                if password1!=password2:
                    return render(request, "register.html", {'msg': '两次密码不一致','captcha_form':captcha_form})
                user_profile = UserProfile()
                user_profile.username = user_name
                user_profile.nick_name = user_name
                user_profile.password = password1
                user_profile.password = make_password(password1)
                user_profile.save()

                messages.success(request, "注册成功")
                return render(request, "login.html")
            else:
                messages.success(request, "用户名或密码错误")
                return render(request, "register.html", {'captcha_form':captcha_form})
        else:
            messages.success(request, "验证码输入错误")#弹出框
            return render(request, "register.html", {'captcha_form':captcha_form})

class LoginoutView(View):
    """
    用户注销
    """
    def get(self, request):
        logout(request)
        return HttpResponseRedirect(reverse("index"))
