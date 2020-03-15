from datetime import datetime

from django.db import models

from user.models import UserProfile
from ScenicSpot.models import ScenicSpot
from DjangoUeditor.models import UEditorField

# Create your models here.

class ScenicSpotComments(models.Model):                 #创建字段
    #景点评论
    user=models.CharField(max_length=50,verbose_name='用户昵称')
    scenicspot= models.CharField(max_length=50,verbose_name="景点名称")
    comments =models.CharField(max_length=2000,verbose_name='评论')
    # 10进制浮点数
    Emotional_score = models.DecimalField(max_digits=10,decimal_places=2,verbose_name="情感得分",default=0)

    add_time= models.DateTimeField(default=datetime.now,verbose_name="添加时间",blank=True,null=True)
    spot_from=models.CharField(max_length=50,verbose_name="来源",default='飞猪')

    class Meta:
        verbose_name = '景点评论'
        verbose_name_plural = verbose_name

    def emotion(self):                          #反馈性质
        if self.Emotional_score>0:
            return "积极"
        elif self.Emotional_score==0:
            return "中性"
        elif self.Emotional_score<0:
            return "消极"


class UserFavorite(models.Model):               #创建字段
    """
    用户收藏
    """
    user=models.CharField(max_length=50,verbose_name='用户昵称')
    fav_spot=models.ForeignKey(ScenicSpot,verbose_name="景点",on_delete=models.CASCADE)
    add_time= models.DateTimeField(default=datetime.now,verbose_name="添加时间",blank=True,null=True)

    class Meta:
        verbose_name = '用户收藏'
        verbose_name_plural = verbose_name


class UserBlog(models.Model):                   #创建字段
    #用户博客
    user=models.ForeignKey(UserProfile,verbose_name='用户',on_delete=models.CASCADE)
    title = models.CharField(max_length=100, verbose_name='标题',blank=True,null=True)
    desc = models.CharField(max_length=500, verbose_name='简介',blank=True,null=True)
    content = models.TextField(verbose_name="内容", default="",blank=True,null=True)
    rich_content = UEditorField(u'富文本内容',width=600, height=300, toolbars="full", imagePath="userblog/blogimages/", filePath="userblog/blogfiles/",
             settings={},command=None,blank=True)
    image = models.ImageField(upload_to="UserBlog/%Y/%m", verbose_name='图片', max_length=100, blank=True, null=True)
    add_time= models.DateTimeField(default=datetime.now,verbose_name="添加时间",blank=True,null=True)

    class Meta:
        verbose_name = '用户博客'
        verbose_name_plural = verbose_name

class UserFavor(models.Model):
    """用户收藏博客"""
    user = models.ForeignKey(UserProfile, verbose_name='用户', on_delete=models.CASCADE)
    blog_id = models.CharField(max_length=100, verbose_name='收藏博客id',blank=True,null=True)
    add_time = models.DateTimeField(default=datetime.now, verbose_name="添加时间", blank=True, null=True)

    class Meta:
        verbose_name = '用户收藏'
        verbose_name_plural = verbose_name