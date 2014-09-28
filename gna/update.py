# -*- coding: utf-8 -*-

from django.conf import settings

import datetime

from gna.gna_normal.models import (
    Player,
    DailyAccessLog,
    PaymentInfo,
)
from gna.common import (
    str_to_date,
    date_to_str,
    str_to_datetime,
    datetime_to_str,
    date_to_datetime_begin,
    date_to_month_begin,
    get_start_date,
    get_month_cache_key,
)
from gna.cache import (
    daily_cache,
    simple_cache,
    delta_cache,
    daily_flag_cache,
)
from gna.job import *


# 上次执行的时间
JOB_DATETIME_BOUND_KEY = 'gna_job_cache_datetime_bound'
def get_job_datetime_bound(db):
    get_cache = simple_cache().get(db, JOB_DATETIME_BOUND_KEY)
    if get_cache:
        return str_to_datetime(get_cache['value'])
    else:
        return date_to_datetime_begin(get_start_date(db))

def set_job_datetime_bound(db, datetime_bound=None):
    if datetime_bound is None:
        datetime_bound = datetime.datetime.now()
    datetime_str = datetime_to_str(datetime_bound)
    simple_cache().set(db, JOB_DATETIME_BOUND_KEY, datetime_str)


# 更新cache
def update_cache(run_limit_datetime_bound=datetime.datetime.now()):
    dbs = settings.GNA_DATABASES

    for db in dbs:
        is_end_the_day = False
        
        pre_global_job_datetime_bound = get_job_datetime_bound(db)
        cur_global_job_datetime_bound = run_limit_datetime_bound
        if cur_global_job_datetime_bound <= pre_global_job_datetime_bound:
            return 'limit'
        # 时间的跨度不会超过到第二天，如果超过第二天当作前一天处理
        cur_global_job_date = pre_global_job_datetime_bound.date()
        
        if pre_global_job_datetime_bound.date() != cur_global_job_datetime_bound.date():
            is_end_the_day = True # 一天结束
            cur_global_job_datetime_bound = date_to_datetime_begin(cur_global_job_date) + datetime.timedelta(days=1)
        
        # table update cache
        for updater in TABLE_UPDATE_LIST:
            updater(db, pre_global_job_datetime_bound, cur_global_job_datetime_bound)
        print pre_global_job_datetime_bound
        print cur_global_job_datetime_bound

        # do jobs        
        for job in JOBS_LIST:
            cache_key = job.__name__[:-4]

            pre_job_datetime_bound = pre_global_job_datetime_bound
            cur_job_datetime_bound = cur_global_job_datetime_bound
            cur_job_date = cur_global_job_date

            # 如果该天刚开始，则对cache初始化
            if pre_job_datetime_bound == date_to_datetime_begin(pre_job_datetime_bound):
                daily_cache().set(db, cache_key, cur_job_date, '0')

            # 是否需要特殊处理
            if not job().is_special:
                para = []
                for key in job().paraments['delta_cache']:
                    para.append(eval(key))
                for key in job().paraments['daily_cache']:
                    value = daily_cache().get(db, key, cur_job_date)['value']
                    para.append(float(value))
                result = job().do_job(*para)
            else:
                para = [db, pre_job_datetime_bound, cur_job_datetime_bound]
                result = job().do_job(*para)
            
            # job结果处理方式
            if job().action == 'inc':
                value = daily_cache().get(db, cache_key, cur_job_date)['value']
                value = str(float(value) + result)
                daily_cache().set(db, cache_key, cur_job_date, value)
            elif job().action == 'replace':
                value = str(result)
                daily_cache().set(db, cache_key, cur_job_date, value)
            elif job().action == 'pass':
                pass
            else:
                raise 'job.action error:%s:%s!' % (job.__name__, str(job().action))

            # month_job处理
            month_cache_key = get_month_cache_key(cache_key, cur_job_date)

            if pre_job_datetime_bound == date_to_datetime_begin(get_start_date(db)) or \
                pre_job_datetime_bound == date_to_month_begin(pre_job_datetime_bound):
                simple_cache().set(db, month_cache_key, '0')

            if job().action == 'inc':
                value = simple_cache().get(db, month_cache_key)['value']
                value = str(float(value) + result)
                simple_cache().set(db, month_cache_key, value)
            elif job().action == 'replace':
                para = []
                for key in job().paraments['daily_cache']:
                    value = simple_cache().get(db, get_month_cache_key(key, cur_job_date))['value']
                    para.append(float(value))
                result = job().do_month_job(*para)
                value = str(result)
                simple_cache().set(db, month_cache_key, value)
            elif job().action == 'pass':
                pass
            else:
                raise 'job.action error:%s:%s!' % (job.__name__, str(job().action))
            
            # 该天结束，将其标记
            if is_end_the_day:
                daily_flag_cache().set(db, cache_key, cur_job_date, True)
            
        # 更新成功
        set_job_datetime_bound(db, cur_job_datetime_bound)

    return 'suc'




##### table update cache #####
TABLE_DAILYACCESSLOG_CACHE = []
TABLE_PAYMENTINFO_CACHE = []
TABLE_PLAYER_CACHE = []
def get_table_dailyaccesslog_cache():
    global TABLE_DAILYACCESSLOG_CACHE
    return TABLE_DAILYACCESSLOG_CACHE

def get_table_paymentinfo_cache():
    global TABLE_PAYMENTINFO_CACHE
    return TABLE_PAYMENTINFO_CACHE

def get_table_player_cache():
    global TABLE_PLAYER_CACHE
    return TABLE_PLAYER_CACHE

def table_dailyaccesslog_update(db, pre_job_datetime_bound, cur_job_datetime_bound):
    global TABLE_DAILYACCESSLOG_CACHE
    TABLE_DAILYACCESSLOG_CACHE = DailyAccessLog.objects.using(db).filter(
            accessed_at__range=(pre_job_datetime_bound, cur_job_datetime_bound)
        ).values()

def table_paymentinfo_update(db, pre_job_datetime_bound, cur_job_datetime_bound):
    global TABLE_PAYMENTINFO_CACHE
    TABLE_PAYMENTINFO_CACHE = PaymentInfo.objects.using(db).filter(
            created_at__range=(pre_job_datetime_bound, cur_job_datetime_bound)
        ).values()

def table_player_update(db, pre_job_datetime_bound, cur_job_datetime_bound):
    global TABLE_PLAYER_CACHE
    TABLE_PLAYER_CACHE = Player.objects.using(db).filter(
            created_at__range=(pre_job_datetime_bound, cur_job_datetime_bound)
        ).values()

TABLE_UPDATE_LIST = []
for key, value in locals().items():
    if key.startswith('table_') and key.endswith('_update'):
        TABLE_UPDATE_LIST.append(value)











