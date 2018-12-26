import os
import sys


DEV_ENV = True
PROD_ENV = False

ROOT_URLCONF = 'FDSops.urls'
WSGI_APPLICATION = 'FDSops.wsgi.application'


AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]



#设置时区
LANGUAGE_CODE = 'zh-hans'  #中文支持，django1.8以后支持；1.8以前是zh-cn
TIME_ZONE = 'Asia/Shanghai'
USE_I18N = True
USE_L10N = True
USE_TZ = False   #默认是Ture，时间是utc时间，由于我们要用本地时间，所用手动修改为false！！！！


if DEV_ENV:
    from .dev_settings import *

if PROD_ENV:
    from .prod_settings import *