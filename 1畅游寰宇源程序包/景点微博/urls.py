"""景点微博 URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path,re_path,include
import xadmin
from django.views.static import serve  # 需要导入

from user.views import IndexView, LoginView, RegisterView, LoginoutView
from operation.views import BlogView,UploadExcel,BlogPublish,BlogDetails,BlogSearchView,Userfavor,Contact,Travel
# from operation.views import SpotSearchView
from ScenicSpot.views import SpotsView,SpotCommentsView,SearchgCommentsView
from .settings import MEDIA_ROOT#,STATIC_ROOT
from django.conf.urls import url
import DjangoUeditor
from django.conf.urls.static import static
from django.conf import settings




urlpatterns = [
    path('xadmin/', xadmin.site.urls,name='xadmin'),

    re_path('media/(?P<path>.*)', serve, {"document_root": MEDIA_ROOT}),#用户上传后的文件一般保存的地方

    path('', IndexView.as_view(), name='index'),
    path('login/', LoginView.as_view(), name='login'),
    path('register/', RegisterView.as_view(), name='register'),
    path('logout/', LoginoutView.as_view(), name="logout"),

    path('spots/', SpotsView.as_view(), name='spots'),
    # path('search_comments/', SearchCommentsView.as_view(), name='search_comments'),
    re_path('spotcomments/(?P<spot_name>.*)', SpotCommentsView.as_view(), name='spotcomments'),
    re_path('spot_comments/(?P<spot_name>.*)/(?P<keyword>.*)', SearchgCommentsView.as_view(), name='searchcomments'),
    path('file/', UploadExcel.as_view(), name='upload'),

    path('blog/', BlogView.as_view(), name='blog'),
    re_path('search_blog/(?P<keyword>.*)', BlogSearchView.as_view(), name='blogsearch'),
    # re_path('search_spot/(?P<keyword>.*)', SpotSearchView.as_view(), name='spotsearch'),
    path('blogpublish/', BlogPublish.as_view(), name='blogpublish'),    #继承View，as_view()自动判断请求方法
    path('userfavor/', Userfavor.as_view(), name='userfavor'),
    #path('about/',About.as_view(), name='about'),
    path('contact/',Contact.as_view(), name='contact'),
    path('travel/',Travel.as_view(),name='travel'),



    re_path('blogdetails/(?P<blog_id>.*)', BlogDetails.as_view(), name='blogdetails'),
    url(r'^captcha/',include('captcha.urls')),
    url(r'^ueditor/',include('DjangoUeditor.urls'))

]+static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)+static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)
