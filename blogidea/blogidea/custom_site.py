from django.contrib.admin import AdminSite


# 自定义site，让文章板块的功能指向这个站点：custom_site.urls
# 而用户管理的后台还是使用之前的site：admin.site.urls
class CustomSite(AdminSite):
    # 页面的展示信息
    site_header = 'Blogtype'    # body中显示的标题
    site_title = 'Blogtype管理后台'     # head中显示的标题
    index_title = '首页'        # head中显示的标题


# 创建自定义站点对象，name属性用于reverse反向解析url的地方
custom_site = CustomSite(name='cus_admin')