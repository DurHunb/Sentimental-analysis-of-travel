from datetime import datetime

from django.db import models

# Create your models here.
class ScenicSpot(models.Model):
    id = models.CharField(max_length=50, verbose_name="景点id",primary_key=True)
    name = models.CharField(max_length=50, verbose_name="景点名称",blank=True,null=True)
    desc = models.CharField(max_length=300, verbose_name='景点描述',blank=True,null=True)
    image = models.ImageField(upload_to="ScenicSpot/%Y/%m", verbose_name='景点图片', max_length=100,blank=True,null=True)
    add_time = models.DateTimeField(default=datetime.now, verbose_name='添加时间',blank=True,null=True)
    type = models.CharField(max_length=100,verbose_name="类型",default="景点")
    times= models.IntegerField(verbose_name="点击次数",default="0")

    class Meta:
        verbose_name = '景点'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name

class Upload(models.Model):
    # 指定上传路径为项目load路径，其中%Y是取当前日期年，%m取当前日期月

    excelname = models.CharField(max_length=10, verbose_name='文件名称')
    add_time = models.DateTimeField(default=datetime.now, verbose_name='添加时间', blank=True, null=True)
    upload_file = models.FileField(upload_to='uploadexcel/%Y/%m', max_length=100, verbose_name='文件上传', null=True, blank=True,)

    # 上传控件报错，ERRORS:
    # practise.Upload.upload_image: (fields.E210) Cannot use ImageField because Pillow is not installed.
    #   HINT: Get Pillow at https://pypi.python.org/pypi/Pillow or run command "pip install Pillow".
    def go_to(self):
        from django.utils.safestring import mark_safe
        # mark_safe后就不会转义
        return mark_safe("<a href='http://101.132.46.114:8000/file'>跳转</a>")

    go_to.short_description = "情感评分"
    class Meta:
        verbose_name = u'评论文件'
        verbose_name_plural = verbose_name

