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
    date_to_datetime_end,
    date_to_month_begin,
    get_start_date,
    get_month_cache_key,
    get_next_month
)
from gna.cache import (
    daily_cache,
    simple_cache,
    delta_cache,
    daily_flag_cache,
)
from gna.job import *
from gna.update import *

def repair(date_list, dbs=settings.GNA_DATABASES):
    for db in dbs:
        if db not in settings.GNA_DATABASES:
            continue
        for the_date in date_list:
            if the_date < get_start_date(db):
                continue

            job_datetime_bound = get_job_datetime_bound(db)
            from_datetime = date_to_datetime_begin(the_date)
            to_datetime = min(date_to_datetime_begin(the_date+datetime.timedelta(days=1)), job_datetime_bound)
            if from_datetime > to_datetime:
                continue
            
            print from_datetime
            print to_datetime

            # daily_flag reset
            daily_flag_cache().set(db, 'retention_ratio', the_date, False)

            # table update cache
            for updater in TABLE_UPDATE_LIST:
                updater(db, from_datetime, to_datetime)

            TABLE_DAILYACCESSLOG_CACHE = get_table_dailyaccesslog_cache()
            TABLE_PAYMENTINFO_CACHE = get_table_paymentinfo_cache()
            TABLE_PLAYER_CACHE = get_table_player_cache()

            # do job
            for job in JOBS_LIST:
                cache_key = job.__name__[:-4]

                # 是否需要特殊处理
                if not job().is_special:
                    para = []
                    for key in job().paraments['delta_cache']:
                        para.append(eval(key))
                    for key in job().paraments['daily_cache']:
                        value = daily_cache().get(db, key, the_date)['value']
                        para.append(float(value))
                    result = job().do_job(*para)
                else:
                    para = [db, from_datetime, to_datetime]
                    result = job().do_job(*para)
                
                # job结果处理方式
                if job().action=='inc' or job().action=='replace':
                    value = str(result)
                    daily_cache().set(db, cache_key, the_date, value)
                elif job().action == 'pass':
                    pass
                else:
                    raise 'job.action error:%s:%s!' % (job.__name__, str(job().action))

                # month_job处理
                month_cache_key = get_month_cache_key(cache_key, the_date)

                from_date = max(get_start_date(db), datetime.date(the_date.year, the_date.month, 1))
                if date_to_datetime_begin(job_datetime_bound.date()) == job_datetime_bound:
                    to_date = job_datetime_bound.date()
                else:
                    to_date = job_datetime_bound.date() + datetime.timedelta(days=1)
                to_date = min(get_next_month(the_date).date(), to_date)

                if job().action == 'inc':
                    result = 0
                    for i in range((to_date-from_date).days):
                        idate = from_date + datetime.timedelta(days=i)
                        try:
                            value = daily_cache().get(db, cache_key, idate)['value']
                        except:
                            #####
                            print cache_key, idate
                        result += float(value)
                    simple_cache().set(db, month_cache_key, result)
                elif job().action == 'replace':
                    para = []
                    for key in job().paraments['daily_cache']:
                        value = simple_cache().get(db, get_month_cache_key(key, the_date))['value']
                        para.append(float(value))
                    result = job().do_month_job(*para)
                    result = str(result)
                    simple_cache().set(db, month_cache_key, result)
                elif job().action == 'pass':
                    pass
                else:
                    raise 'job.action error:%s:%s!' % (job.__name__, str(job().action))
















