__date__ = '2019/3/7 22:34'
import xadmin
from .models import UserBlog,UserFavor


class UserBlogAdmin(object):
    list_display = ['user', 'title','content', 'add_time']
    search_fields = ['user', 'title','content']
    list_filter = ['user', 'title','content', 'add_time']

    style_fields = {'rich_content': 'ueditor'}
#加上了图片才能显示出来

class UserFavorAdmin(object):
    list_display = ['user', 'blog_id', 'add_time']
    search_fields = ['user', 'blog_id']
    list_filter = ['user', 'blog_id', 'add_time']


xadmin.site.register(UserBlog, UserBlogAdmin)
xadmin.site.register(UserFavor, UserFavorAdmin)