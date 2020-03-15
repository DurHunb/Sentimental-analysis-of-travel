import xadmin
from xadmin import views

class BaseSetting(object):
    # 选择模式
    enable_themes = True
    # 调用主题菜单
    use_bootswatch = True


class GlobalSettings(object):
    site_title="畅游寰宇网站后台管理系统"
    site_footer='畅游寰宇'
    menu_style='accordion'

xadmin.site.register(views.BaseAdminView,BaseSetting)
xadmin.site.register(views.CommAdminView,GlobalSettings)
