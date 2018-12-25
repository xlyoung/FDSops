import os
import sys



# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, BASE_DIR)
sys.path.insert(0, os.path.join(BASE_DIR, 'apps'))
sys.path.insert(0, os.path.join(BASE_DIR, 'extra_apps'))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'k+m2t9w4ulc56jy2@@0#53%uk#wdsvz0s1f3ie8wy88b1y0b0x'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['*']
AUTH_USER_MODEL = 'users.UserProfile'

# Application definition

INSTALLED_APPS = [
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'users.apps.UsersConfig',
    'media_files.apps.MediaFilesConfig',
    'DjangoUeditor',
    'corsheaders',
    'xadmin',
    'crispy_forms',
    'rest_framework',
    'django_filters',
]

MIDDLEWARE = [
    "utils.disable_csrf.DisableCSRFCheck",
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'FDSops.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')]
        ,
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'FDSops.wsgi.application'


# Database
# https://docs.djangoproject.com/en/2.1/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': "fdsops",
        'USER': 'root',
        'PASSWORD': "123456",
        'HOST': "127.0.0.1",
        "OPTIONS": {"init_command": "SET default_storage_engine=INNODB;"}
    }
}



# Password validation
# https://docs.djangoproject.com/en/2.1/ref/settings/#auth-password-validators

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


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.1/howto/static-files/


STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, "static/")



MEDIA_URL = "/media/"
# STATICFILES_DIRS = (
#     os.path.join(BASE_DIR, "static"),
# )

MEDIA_ROOT = os.path.join(BASE_DIR, "media")

#fds客户端配置
CONFIG_ROOT = os.path.join(BASE_DIR, "config")

#上传限制
DATA_UPLOAD_MAX_NUMBER_FIELDS = 10240

##域名
WEB_HOST_NAME = "http://127.0.0.1"

#限制图片大小
#20M
IMAGE_SIZE_LIMIT = 20000000

#限制图片类型
TYPE_LIST = ["png", "jpeg", "jpg"]

# 设置Django的文件存储类
DEFAULT_FILE_STORAGE= 'utils.fds_storage.FDFSStorage'

# 设置fdfs使用的client.conf文件路径
FDFS_CLIENT_CONF= CONFIG_ROOT + "/client.conf"

# 设置fdfs存储服务器上nginx的IP和端口号
FDFS_URL='http://192.168.1.151:38080/'



REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework.authentication.BasicAuthentication',
        'rest_framework.authentication.SessionAuthentication',
        'rest_framework_jwt.authentication.JSONWebTokenAuthentication',
    ),

}


AUTHENTICATION_BACKENDS = (
    'users.views.CustomBackend',
)

#jwt认证时间
import datetime
JWT_AUTH = {
    'JWT_EXPIRATION_DELTA': datetime.timedelta(days=7),
    'JWT_AUTH_HEADER_PREFIX': 'JWT',
}


#手机号码正则表达式
REGEX_MOBILE = "^1[358]\d{9}$|^147\d{8}$|^176\d{8}$"

#邮箱地址正则表达式
REGEX_EMAIL= "^[a-zA-Z0-9_-]+(\.[a-zA-Z0-9_-]+){0,4}@[a-zA-Z0-9_-]+(\.[a-zA-Z0-9_-]+){0,4}$"


#解决跨域问题
CORS_ORIGIN_ALLOW_ALL = True


EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.exmail.qq.com'
EMAIL_PORT = 465
#发送邮件的邮箱
EMAIL_HOST_USER = 'noreply@fastersoft.com.cn'
#在邮箱中设置的客户端授权密码
EMAIL_HOST_PASSWORD = '(IJN0okm'
#收件人看到的发件人
DEFAULT_FROM_EMAIL = '东华发思特<noreply@fastersoft.com.cn>'
EMAIL_USE_SSL = True


# #日志
# LOGGING = {
#     'version': 1,
#     'disable_existing_loggers': False,
#     'formatters': {
#         'verbose': {
#             'format': '[%(levelname)1.1s %(asctime)s %(module)s:%(lineno)d] %(message)s',
#             'datefmt': '%Y%m%d %H:%M:%S',
#         },
#     },
#     'handlers': {
#         'file': {
#             'level': 'INFO',
#             'class': 'logging.FileHandler',
#             'formatter': 'verbose',
#             'filename': '%s/error.logs'%BASE_DIR,
#         },
#     },
#     'loggers': {
#         'django': {
#             'handlers': ['file'],
#             'level': 'INFO',
#             'propagate': True,
#         },
#     },
# }