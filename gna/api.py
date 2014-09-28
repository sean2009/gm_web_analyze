# -*- coding: utf-8 -*-

from django.conf import settings

import datetime

from gna.common import (
    get_retention_cache_key,
    get_month_cache_key,
)
from gna.gna_normal.models import (
    Player,
    DailyAccessLog,
    PaymentInfo,
)
from gna.cache import (
    daily_cache,
    simple_cache,
    delta_cache,
    daily_flag_cache,
)

def _get_month_cache(db, key, date):
    cache_key = get_month_cache_key(key, date)
    cache = simple_cache().get(db, cache_key)
    if cache:
        return cache['value']
    else:
        return None

def _get_date_str(date):
    if type(date)==datetime.date or type(date)==datetime.datetime:
        return date.strftime('%Y-%m-%d')
    return date

def _get_str_by_int(value):
    if value != None:
        return str(int(float(value)))
    else:
        return None

def _get_str_by_float(value):
    if value != None:
        return '%.1f' % (float(value))
    else:
        return None

def _get_percent_by_float(value):
    if value != None:
        return '%.1f%%' % (float(value)*100.0)
    else:
        return None

# GNA Daily 
class GNAObject(object):
    income = None
    dau = None
    arpu = None
    arppu = None
    pay_user = None
    pay_ratio = None
    first_pay_user = None
    first_pay_ratio = None
    register_user = None

    def __init__(self, db, date):
        self.db = db
        self.date = date

    def get_str(self):      
        self.date_str = _get_date_str(self.date)       
        self.income_str = _get_str_by_int(self.income)
        self.dau_str = _get_str_by_int(self.dau)
        self.arpu_str = _get_str_by_float(self.arpu)
        self.arppu_str = _get_str_by_float(self.arppu)
        self.pay_user_str = _get_str_by_int(self.pay_user)
        self.pay_ratio_str = _get_percent_by_float(self.pay_ratio)
        self.first_pay_user_str = _get_str_by_int(self.first_pay_user)
        self.first_pay_ratio_str = _get_percent_by_float(self.first_pay_ratio)
        self.register_user_str = _get_str_by_int(self.register_user)

def get_gna_objs_list(db, from_date, to_date):
    income_data = daily_cache().get_by_date_range(db, 'income', from_date, to_date)
    dau_data = daily_cache().get_by_date_range(db, 'dau', from_date, to_date)
    arpu_data = daily_cache().get_by_date_range(db, 'arpu', from_date, to_date)
    arppu_data = daily_cache().get_by_date_range(db, 'arppu', from_date, to_date)
    pay_user_data = daily_cache().get_by_date_range(db, 'pay_user', from_date, to_date)
    pay_ratio_data = daily_cache().get_by_date_range(db, 'pay_ratio', from_date, to_date)
    first_pay_user_data = daily_cache().get_by_date_range(db, 'first_pay_user', from_date, to_date)
    first_pay_ratio_data = daily_cache().get_by_date_range(db, 'first_pay_ratio', from_date, to_date)
    register_user_data = daily_cache().get_by_date_range(db, 'register_user', from_date, to_date)

    objs = []
    obj_dict = {}
    for i in range((to_date - from_date).days + 1):
        date = from_date + datetime.timedelta(days=i)
        obj = GNAObject(db, date)
        obj_dict[date] = obj
        objs.append(obj)

    objs.reverse()

    for data in income_data:
        date, value = data['date'], data['value']
        obj_dict[date].income = value

    for data in dau_data:
        date, value = data['date'], data['value']
        obj_dict[date].dau = value

    for data in arpu_data:
        date, value = data['date'], data['value']
        obj_dict[date].arpu = value

    for data in arppu_data:
        date, value = data['date'], data['value']
        obj_dict[date].arppu = value

    for data in pay_user_data:
        date, value = data['date'], data['value']
        obj_dict[date].pay_user = value

    for data in pay_ratio_data:
        date, value = data['date'], data['value']
        obj_dict[date].pay_ratio = value

    for data in first_pay_user_data:
        date, value = data['date'], data['value']
        obj_dict[date].first_pay_user = value

    for data in first_pay_ratio_data:
        date, value = data['date'], data['value']
        obj_dict[date].first_pay_ratio = value

    for data in register_user_data:
        date, value = data['date'], data['value']
        obj_dict[date].register_user = value

    for obj in objs:
        obj.get_str()

    return objs

# GNA Month
def get_gna_month_obj(db, date):
    obj = GNAObject(db, date)

    obj.income = float(_get_month_cache(db, 'income', date))
    obj.dau = float(_get_month_cache(db, 'dau', date))
    obj.arpu = float(_get_month_cache(db, 'arpu', date))
    obj.arppu = float(_get_month_cache(db, 'arppu', date))
    obj.pay_ratio = float(_get_month_cache(db, 'pay_ratio', date))
    obj.pay_user = float(_get_month_cache(db, 'pay_user', date))
    obj.first_pay_user = float(_get_month_cache(db, 'first_pay_user', date))
    obj.first_pay_ratio = float(_get_month_cache(db, 'first_pay_ratio', date))
    obj.register_user = float(_get_month_cache(db, 'register_user', date))

    obj.get_str()
    return obj

# Retention Daily
class RetentionObject(object):
    retention_ratio1_str = None
    retention_ratio2_str = None
    retention_ratio3_str = None
    retention_ratio4_str = None
    retention_ratio5_str = None
    retention_ratio6_str = None
    retention_ratio7_str = None
    retention_ratio14_str = None
    retention_ratio30_str = None
    retention_ratio60_str = None
    retention_ratio90_str = None

    def __init__(self, db, date):
        self.db = db
        self.date = date
        self.date_str = _get_date_str(self.date)

def get_retention_ratio_daily_objs_list(db, from_date, to_date):
    days_list = settings.GNA_RETENTION_DAYS_LIST

    objs = []
    obj_dict = {}
    for i in range((to_date - from_date).days + 1):
        date = from_date + datetime.timedelta(days=i)
        obj = RetentionObject(db, date)
        obj_dict[date] = obj
        objs.append(obj)

    objs.reverse()

    for days in days_list:
        cache_key = get_retention_cache_key('retention_ratio', days)
        cache_data = daily_cache().get_by_date_range(db, cache_key, from_date, to_date)

        for data in cache_data:
            date, value = data['date'], data['value']
            obj = obj_dict[date]
            setattr(obj, 'retention_ratio%d_str'%days, value)

    return objs

def get_retention_ratio_daily_objs_list_2(db, from_date, to_date):
    days_list = settings.GNA_RETENTION_DAYS_LIST

    objs = []
    obj_dict = {}
    for i in range((to_date - from_date).days + 1):
        date = from_date + datetime.timedelta(days=i)
        obj = RetentionObject(db, date)
        obj_dict[date] = obj
        objs.append(obj)

    objs.reverse()

    for days in days_list:
        cache_key = get_retention_cache_key('retention_ratio', days)
        cache_data = daily_cache().get_by_date_range(db, cache_key, from_date+datetime.timedelta(days=days), to_date+datetime.timedelta(days=days))

        for data in cache_data:
            date, value = data['date']-datetime.timedelta(days=days), data['value']
            obj = obj_dict[date]
            setattr(obj, 'retention_ratio%d_str'%days, value)

    return objs
