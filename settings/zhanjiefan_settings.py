# -*- coding: utf-8 -*-
import os
from settings.gna_settings import *

TABULATE_WEB_LIST_DAILY_DATE_LIMIT = 10
TABULATE_WEB_LIST_DAILY_PLATFORM_DATE_LIMIT = 10
TABULATE_WEB_LIST_DAILY_CHANNEL_DATE_LIMIT = 10

##### MySQL DB #####
MYSQL_DB_USER = 'root'
MYSQL_DB_PASS = 'root'

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
        'NAME': 'dev01_brave_cn_gna',
        'USER': 'zhangxiaohui',
        'PASSWORD': 'gumichina',
        'HOST': '10.6.30.44',
        'PORT': '3306',
    },
    'tabulate': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'kpi',
        'USER': 'zhangxiaohui',
        'PASSWORD': 'gumichina',
        'HOST': '10.6.30.44',
        'PORT': '3306',
    },
    'dev01_brave_cn_common': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'dev01_brave_cn_common',
        'USER': 'zhangxiaohui',
        'PASSWORD': 'gumichina',
        'HOST': '10.6.30.44',
        'PORT': '3306',
    },
}

##### GNA #####
GNA_DATABASES = [
    'gz01',
]
GNA_START_DATE = {
    # gna
    'default': '2014-08-23',
    'gz01': '2014-09-07',

    # tabulate
    'tabulate': '2014-09-01',
}
GNA_DATABASE_NAME = {
    # gna
    'default': 'default_name',
    'gz01': '勇者归来',

    # tabulate
    'tabulate': '',
}