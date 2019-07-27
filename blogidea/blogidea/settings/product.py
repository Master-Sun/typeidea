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
        'CONN_MAX_AGE': 60,
        # 配置数据库连接的字符集
        'OPTIONS': {'charset': 'utf8mb4'},
    },
}

# 配置redis缓存
REDIS_URL = '127.0.0.1:6379:1'

CACHES = {
    'default': {
        'BACKEND': 'django_redis.cache.RedisCache',
        'LOCATION': REDIS_URL,
        'TIMEOUT': 300,
        'OPTIONS': {
            # 'PASSWORD': '****',
            'CLIENT_CLASS': 'django_redis.client.DefaultClient',
            'PARSER_CLASS': 'redis.connection.HiredisParser',
        },
        'CONNECTION_POOL_CLASS': 'redis.connection.BlockingConnectionPool',
    }
}

# CACHES = {
#     'default': {
#         'BACKEND': 'django.core.cache.backends.memcached.MemcachedCache',
#         'LOCATION': [
#             # Memcached系统的主机地址
#             '127.0.0.1:11211',
#             '172.19.26.242:11211',
#         ]
#     }
# }