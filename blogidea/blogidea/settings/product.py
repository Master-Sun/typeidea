from .base import *

DEBUG = False

ALLOWED_HOSTS = ['*',]

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'typeidea_sk',
        'USER': 'sk',
        'PASSWORD': '123456',
        'HOST': '119.3.4.159',
        'PORT': 3306,
        # 配置django和数据库的持久化连接，默认值为0
        'CONN_MAX_AGE': 5 * 60,
        # 配置数据库连接的字符集
        'OPTIONS': {'charset': 'utf8mb4'},
    },
}