__date__ = '2019/3/7 22:34'
import xadmin
from .models import ScenicSpot,Upload
from xadmin.views import CommAdminView
from operation.views import UploadExcel

class ScenicSpotAdmin(object):
    list_display=['name','desc','add_time','times']
    search_fields=['name','desc']
    list_filter=['name','add_time','type']

    #显示详情
    show_detail_fields=['name']
    #数据刷新时间
    refresh_times=(3,5)
xadmin.site.register(ScenicSpot,ScenicSpotAdmin)

class UploadAdmin(object):
    list_display = ['excelname','add_time','go_to']  # 控制显示列数　　
    search_fields = ['excelname']  # 控制搜索框的显示
    list_filter = ['excelname','add_time']  # 控制筛选


xadmin.site.register(Upload, UploadAdmin)







