from .base import *    # NOQA


DEBUG = True

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}

# 配置第三方性能优化插件：django-debug-toolbar
# 该工具只能在开发和测试阶段使用，只有在DEBUG=True时才会生效
# 因此添加在develop.py而不是base.py
INSTALLED_APPS += [
    'debug_toolbar',
]

MIDDLEWARE += [
    'debug_toolbar.middleware.DebugToolbarMiddleware',
]

INTERNAL_IPS = ['127.0.0.1',]

# 工具的显示依赖jquery，如果前端无法显示可指定jquery地址
DEBUG_TOOLBAR_CONFIG = {
        'JQUERY_URL': '/static/js/jquery3.4.1.js',
        # 'JQUERY_URL': '//cdn.bootcss.com/jquery/2.1.4/jquery.min.js',
        # 'SHOW_COLLAPSED': True,
        # 'SHOW_TOOLBAR_CALLBACK': lambda x: True,
    }
