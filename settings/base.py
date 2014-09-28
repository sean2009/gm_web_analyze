# -*- coding: utf-8 -*-
import os
import warnings

BASE_DIR = os.path.dirname(os.path.dirname(__file__))

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.6/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'g7m^(=3_@yw-=k220dcpz=vh_p3be0zl#dn@-fj&xs*e0a%i@0'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

TEMPLATE_DEBUG = True

ALLOWED_HOSTS = []

##### filter warnings #####
# warnings.filterwarnings(
#         'error', r"DateTimeField .* received a naive datetime",
#         RuntimeWarning, r'django\.db\.models\.fields')

##### Internationalization #####
LANGUAGE_CODE = 'zh-cn'
TIME_ZONE = 'Asia/Shanghai'
USE_I18N = True
USE_L10N = True
#USE_TZ = True

##### Static #####
MEDIA_ROOT = '../media'
MEDIA_URL = '/media/'
STATIC_ROOT = '../static'
STATIC_URL = '/static/'

STATICFILES_FINDERS = (   
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
#    'django.contrib.staticfiles.finders.DefaultStorageFinder',
)

STATICFILES_DIRS = (
    #os.path.join(BASE_DIR, "static"),
)

##### Application #####
INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # my app
    'gna',
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

ROOT_URLCONF = 'web_analyze.urls'

WSGI_APPLICATION = 'web_analyze.wsgi.application'

##### Template #####
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
#     'django.template.loaders.eggs.Loader',
)

TEMPLATE_DIRS = (
    # Put strings here, like "/home/html/django_templates" or "C:/www/django/templates".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
)

CONTEXT_PROCESSORS = (
    'django.core.context_processors.csrf'
)

##### MySQL DB #####
MYSQL_DB_USER = 'root'
MYSQL_DB_PASS = 'gumichina0521'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'web_analyze_main',
        'USER': MYSQL_DB_USER,
        'PASSWORD': MYSQL_DB_PASS,
        'HOST': '',
        'PORT': '',
    },
    'gz01': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'pro_android_gz01_brave_cn_gna',
        'USER': 'zhangxiaohui',
        'PASSWORD': 'gumichina',
        'HOST': '10.6.31.118',
        'PORT': '',
    },
    'gz02': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'pro_android_gz02_brave_cn_gna',
        'USER': 'zhangxiaohui',
        'PASSWORD': 'gumichina',
        'HOST': '10.6.31.118',
        'PORT': '',
    },
    'tabulate': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'kpi',
        'USER': 'zhangxiaohui',
        'PASSWORD': 'gumichina',
        'HOST': '10.6.31.118',
        'PORT': '',
    },
    'pro_android_gz01_brave_cn_common': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'pro_android_gz01_brave_cn_common',
        'USER': 'zhangxiaohui',
        'PASSWORD': 'gumichina',
        'HOST': '10.6.31.118',
        'PORT': '',
    },
}

##### GNA #####
GNA_DATABASES = [
    'gz01',
]
GNA_START_DATE = {
    # gna
    'gz01': '2014-09-11',

    # tabulate
    'tabulate': '2014-09-11',
}
GNA_DATABASE_NAME = {
    # gna
    'gz01': '越狱1区-勇者归来',
    'gz02': '越狱2区-扬帆起航',

    # tabulate
    'tabulate': '',
}
# tabulate_date database
TABULATE_DATABASE = [
    'tabulate',
]
TABULATE_ZONE_LIST = [
    'summary',
    'pro_android_gz01',   
]

TABULATE_ZONE_NAME = {
    'summary': '汇总',
    'pro_android_gz01': '越狱1区-勇者归来',
    'pro_android_gz02': '越狱2区-扬帆起航',
}
TABULATE_PLATFORM_LIST = [
    4, 
    1, 
    5, 
    3, 
    2,
]
TABULATE_PLATFORM_NAME = {
    1: 'Ios正版',
    2: 'GOOGLE PLAY',
    3: 'KINDLE',
    4: '安卓国内',
    5: 'Ios越狱',
}
TABULATE_CHANNEL_LIST = [
    '999999',
    '500003',
    '500015',
    '500001',
    '500002',
    '000023',
    '000215',
    '000116',
    '000016',
    '000020',
    '000255',
    '000007',
    '000056',
    '000013',
    '000032',
    '000266',
    '000065',
    '000066',
    '000072',
    '000908',
    '000247',
    '000003',
    '000000',
    '000005',
    '000008',
    '000002',
    '000054',
    '000009',
    '900084',
    '900037',
    '900038',
    '200028',
    '000491',
    '000550',
    '000004',
    '000222',
    '200057',
    '000441',
    '000012',
    '000286',
    '900101',
    '900100',
]
TABULATE_CHANNEL_NAME = {
    '999999': 'test',
    '500003': 'PP助手',
    '500015': '快用苹果',
    '500001': '91助手',
    '500002': '同步推',
    '000023': '360手机助手',
    '000215': '百度多酷',
    '000116': '豌豆荚',
    '000016': '联想',
    '000020': 'OPPO',
    '000255': 'UC',
    '000007': '91助手',
    '000056': '联通',
    '000013': '移动MM',
    '000032': '电信爱游戏',
    '000266': '移动游戏基地',
    '000065': '联通',
    '000066': '小米',
    '000072': '3G',
    '000908': '琵琶网',
    '000247': '拇指玩',
    '000003': '当乐',
    '000000': '触控',
    '000005': '安智',
    '000008': '木蚂蚁',
    '000002': '机锋',
    '000054': '华为',
    '000009': '应用汇',
    '900084': '触控流量中心',
    '900037': 'PunchBox广告平台',
    '900038': '触控广告平台',
    '200028': '智乐',
    '000491': '新浪微游戏',
    '000550': '腾讯应用宝',
    '000004': 'N多',
    '000222': '巴士商店',
    '200057': '步步高',
    '000441': '金山电池',
    '000012': '三星应用商店',
    '000286': '金立游戏中心',
    '900101': '勇者官网',
    '900100': '勇者流量中心免流量',
}


