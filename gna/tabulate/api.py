# -*- coding: utf-8 -*-
import datetime

from gna.tabulate.models import *
from gna.common import (
    div_operation,
)

def _get_date_str(date):
    if type(date)==datetime.date or type(date)==datetime.datetime:
        return date.strftime('%Y-%m-%d')
    return date

def _get_date_by_str(date_str):
    return datetime.datetime.strptime(date_str, '%Y-%m-%d')

def _get_str_by_int(value):
    if value:
        return str(int(value))
    else:
        return None

def _get_str_by_float(value):
    if value:
        return '%.1f' % (value)
    else:
        return None

def _get_percent_by_float(value):
    if value:
        return '%.1f%%' % (value*100.0)
    else:
        return None

class DateCountObject(object):
    device_count = None
    user_count = None
    user_login = None
    dau = None
    vip_count = None
    vip_amount = None
    vip_ratio = None
    arppu = None
    purchase_suc_ratio = None
    lc1 = None
    lc2 = None
    lc3 = None
    lc4 = None
    lc5 = None
    lc6 = None
    lc7 = None
    lc14 = None
    lc30 = None
    lc1_ratio = None
    lc2_ratio = None
    lc3_ratio = None
    lc4_ratio = None
    lc5_ratio = None
    lc6_ratio = None
    lc7_ratio = None
    lc14_ratio = None
    lc30_ratio = None

    def __init__(self, db, date):
        self.db = db
        self.date = date       

    def get_str(self):
        self.date_str = _get_date_str(self.date)
        self.device_count_str = _get_str_by_int(self.device_count)
        self.user_count_str = _get_str_by_int(self.user_count)
        self.user_login_str = _get_str_by_int(self.user_login)
        self.dau_str = _get_str_by_int(self.dau)
        self.vip_count_str = _get_str_by_int(self.vip_count)
        self.vip_amount_str = _get_str_by_int(self.vip_amount)
        self.vip_ratio_str = _get_percent_by_float(self.vip_ratio)
        self.arppu_str = _get_str_by_float(self.arppu)
        self.purchase_suc_ratio_str = _get_percent_by_float(self.purchase_suc_ratio)
        self.lc1_str = _get_str_by_int(self.lc1)
        self.lc2_str = _get_str_by_int(self.lc2)
        self.lc3_str = _get_str_by_int(self.lc3)
        self.lc4_str = _get_str_by_int(self.lc4)
        self.lc5_str = _get_str_by_int(self.lc5)
        self.lc6_str = _get_str_by_int(self.lc6)
        self.lc7_str = _get_str_by_int(self.lc7)
        self.lc14_str = _get_str_by_int(self.lc14)
        self.lc30_str = _get_str_by_int(self.lc30)
        self.lc1_ratio_str = _get_percent_by_float(self.lc1_ratio)
        self.lc2_ratio_str = _get_percent_by_float(self.lc2_ratio)
        self.lc3_ratio_str = _get_percent_by_float(self.lc3_ratio)
        self.lc4_ratio_str = _get_percent_by_float(self.lc4_ratio)
        self.lc5_ratio_str = _get_percent_by_float(self.lc5_ratio)
        self.lc6_ratio_str = _get_percent_by_float(self.lc6_ratio)
        self.lc7_ratio_str = _get_percent_by_float(self.lc7_ratio)
        self.lc14_ratio_str = _get_percent_by_float(self.lc14_ratio)
        self.lc30_ratio_str = _get_percent_by_float(self.lc30_ratio)

class PlatformCountObject(DateCountObject):
    def __init__(self, db, date, platform):
        self.db = db
        self.date = date
        self.platform = platform

class ChannelCountObject(DateCountObject):
    def __init__(self, db, date, channel):
        self.db = db
        self.date = date
        self.channel = channel

def get_date_count_objs_list(db, from_date, to_date, desc=False):
    device_count_data = DeviceCount.objects.using(db).filter(date__range=(from_date, to_date))
    user_count_data = UserCount.objects.using(db).filter(date__range=(from_date, to_date))
    user_login_data = UserLogin.objects.using(db).filter(date__range=(from_date, to_date))
    dau_data = Dau.objects.using(db).filter(date__range=(from_date, to_date))
    vip_count_data = VipCount.objects.using(db).filter(date__range=(from_date, to_date))
    vip_amount_data = VipAmount.objects.using(db).filter(date__range=(from_date, to_date))
    purchase_data = Purchase.objects.using(db).filter(date__range=(from_date, to_date))
    lc1_data = Lc1.objects.using(db).filter(date__range=(from_date+datetime.timedelta(days=1), to_date+datetime.timedelta(days=1)))
    lc2_data = Lc2.objects.using(db).filter(date__range=(from_date+datetime.timedelta(days=2), to_date+datetime.timedelta(days=2)))
    lc3_data = Lc3.objects.using(db).filter(date__range=(from_date+datetime.timedelta(days=3), to_date+datetime.timedelta(days=3)))
    lc4_data = Lc4.objects.using(db).filter(date__range=(from_date+datetime.timedelta(days=4), to_date+datetime.timedelta(days=4)))
    lc5_data = Lc5.objects.using(db).filter(date__range=(from_date+datetime.timedelta(days=5), to_date+datetime.timedelta(days=5)))
    lc6_data = Lc6.objects.using(db).filter(date__range=(from_date+datetime.timedelta(days=6), to_date+datetime.timedelta(days=6)))
    lc7_data = Lc7.objects.using(db).filter(date__range=(from_date+datetime.timedelta(days=7), to_date+datetime.timedelta(days=7)))
    lc14_data = Lc14.objects.using(db).filter(date__range=(from_date+datetime.timedelta(days=14), to_date+datetime.timedelta(days=14)))
    lc30_data = Lc30.objects.using(db).filter(date__range=(from_date+datetime.timedelta(days=30), to_date+datetime.timedelta(days=30)))

    objs = []
    obj_dict = {}
    for i in range((to_date - from_date).days + 1):
        the_date = from_date + datetime.timedelta(days=i)
        obj = DateCountObject(db, the_date)
        objs.append(obj)
        obj_dict[_get_date_str(the_date)] = obj

    # device_count
    for data in device_count_data:
        date, cnt = data.date, data.cnt
        obj_dict[date].device_count = cnt

    # user_count
    for data in user_count_data:
        date, cnt = data.date, data.cnt
        obj_dict[date].user_count = cnt

    # user_login
    for data in user_login_data:
        date, cnt = data.date, data.cnt
        obj_dict[date].user_login = cnt

    # dau
    for data in dau_data:
        date, cnt = data.date, data.cnt
        obj_dict[date].dau = cnt

    # vip_count
    for data in vip_count_data:
        date, cnt = data.date, data.cnt
        obj_dict[date].vip_count = cnt

    # vip_amount
    for data in vip_amount_data:
        date, cnt = data.date, data.cnt
        obj_dict[date].vip_amount = cnt

    # purchase_suc_ratio
    for data in purchase_data:
        date, suc, fail = data.date, data.suc, data.fail
        if suc!=None and fail!=None:
            obj_dict[date].purchase_suc_ratio = div_operation(suc, suc+fail)

    # lc1
    for data in lc1_data:
        date, cnt = _get_date_str(_get_date_by_str(data.date)-datetime.timedelta(days=1)), data.cnt
        obj_dict[date].lc1 = cnt

    # lc2
    for data in lc2_data:
        date, cnt = _get_date_str(_get_date_by_str(data.date)-datetime.timedelta(days=2)), data.cnt
        obj_dict[date].lc2 = cnt

    # lc3
    for data in lc3_data:
        date, cnt = _get_date_str(_get_date_by_str(data.date)-datetime.timedelta(days=3)), data.cnt
        obj_dict[date].lc3 = cnt

    # lc4
    for data in lc4_data:
        date, cnt = _get_date_str(_get_date_by_str(data.date)-datetime.timedelta(days=4)), data.cnt
        obj_dict[date].lc4 = cnt

    # lc5
    for data in lc5_data:
        date, cnt = _get_date_str(_get_date_by_str(data.date)-datetime.timedelta(days=5)), data.cnt
        obj_dict[date].lc5 = cnt

    # lc6
    for data in lc6_data:
        date, cnt = _get_date_str(_get_date_by_str(data.date)-datetime.timedelta(days=6)), data.cnt
        obj_dict[date].lc6 = cnt

    # lc7
    for data in lc7_data:
        date, cnt = _get_date_str(_get_date_by_str(data.date)-datetime.timedelta(days=7)), data.cnt
        obj_dict[date].lc7 = cnt

    # lc14
    for data in lc14_data:
        date, cnt = _get_date_str(_get_date_by_str(data.date)-datetime.timedelta(days=14)), data.cnt
        obj_dict[date].lc14 = cnt

    # lc30
    for data in lc30_data:
        date, cnt = _get_date_str(_get_date_by_str(data.date)-datetime.timedelta(days=30)), data.cnt
        obj_dict[date].lc30 = cnt

    for i in range((to_date - from_date).days + 1):
        the_date = _get_date_str(from_date + datetime.timedelta(days=i))
        obj = obj_dict[the_date]
    
    # vip ratio
        if obj.vip_count and obj.dau:
            obj.vip_ratio = div_operation(int(obj.vip_count), int(obj.dau))
    
    # arppu
        if obj.vip_amount and obj.vip_count:
            obj.arppu = div_operation(int(obj.vip_amount), int(obj.vip_count))

    # lc1_ratio
        if obj.lc1 and obj.device_count:
            obj.lc1_ratio = div_operation(int(obj.lc1), int(obj.device_count))

    # lc2_ratio
        if obj.lc2 and obj.device_count:
            obj.lc2_ratio = div_operation(int(obj.lc2), int(obj.device_count))

    # lc3_ratio
        if obj.lc3 and obj.device_count:
            obj.lc3_ratio = div_operation(int(obj.lc3), int(obj.device_count))

    # lc4_ratio
        if obj.lc4 and obj.device_count:
            obj.lc4_ratio = div_operation(int(obj.lc4), int(obj.device_count))

    # lc5_ratio
        if obj.lc5 and obj.device_count:
            obj.lc5_ratio = div_operation(int(obj.lc5), int(obj.device_count))

    # lc6_ratio
        if obj.lc6 and obj.device_count:
            obj.lc6_ratio = div_operation(int(obj.lc6), int(obj.device_count))

    # lc7_ratio
        if obj.lc7 and obj.device_count:
            obj.lc7_ratio = div_operation(int(obj.lc7), int(obj.device_count))

    # lc14_ratio
        if obj.lc14 and obj.device_count:
            obj.lc14_ratio = div_operation(int(obj.lc14), int(obj.device_count))

    # lc30_ratio
        if obj.lc30 and obj.device_count:
            obj.lc30_ratio = div_operation(int(obj.lc30), int(obj.device_count))
    # get_str
        obj.get_str()

    if not desc:
        objs.reverse()

    return objs

def get_date_platform_count_objs_list(db, date, platform_list):
    device_count_data = PlatformDeviceCount.objects.using(db).filter(date=date, platform__in=platform_list)
    user_count_data = PlatformUserCount.objects.using(db).filter(date=date, platform__in=platform_list)
    user_login_data = PlatformUserLogin.objects.using(db).filter(date=date, platform__in=platform_list)
    dau_data = PlatformDau.objects.using(db).filter(date=date, platform__in=platform_list)
    vip_count_data = PlatformVipCount.objects.using(db).filter(date=date, platform__in=platform_list)
    vip_amount_data = PlatformVipAmount.objects.using(db).filter(date=date, platform__in=platform_list)
    purchase_data = PlatformPurchase.objects.using(db).filter(date=date, platform__in=platform_list)
    lc1_data = PlatformLc1.objects.using(db).filter(date=date+datetime.timedelta(days=1), platform__in=platform_list)
    lc2_data = PlatformLc2.objects.using(db).filter(date=date+datetime.timedelta(days=2), platform__in=platform_list)
    lc3_data = PlatformLc3.objects.using(db).filter(date=date+datetime.timedelta(days=3), platform__in=platform_list)
    lc4_data = PlatformLc4.objects.using(db).filter(date=date+datetime.timedelta(days=4), platform__in=platform_list)
    lc5_data = PlatformLc5.objects.using(db).filter(date=date+datetime.timedelta(days=5), platform__in=platform_list)
    lc6_data = PlatformLc6.objects.using(db).filter(date=date+datetime.timedelta(days=6), platform__in=platform_list)
    lc7_data = PlatformLc7.objects.using(db).filter(date=date+datetime.timedelta(days=7), platform__in=platform_list)
    lc14_data = PlatformLc14.objects.using(db).filter(date=date+datetime.timedelta(days=14), platform__in=platform_list)
    lc30_data = PlatformLc30.objects.using(db).filter(date=date+datetime.timedelta(days=30), platform__in=platform_list)

    objs = []
    obj_dict = {}
    for platform in platform_list:
        obj = PlatformCountObject(db, date, platform)
        objs.append(obj)
        obj_dict[platform] = obj

    # device_count
    for data in device_count_data:
        platform, cnt = data.platform, data.cnt
        obj_dict[platform].device_count = cnt

    # user_count
    for data in user_count_data:
        platform, cnt = data.platform, data.cnt
        obj_dict[platform].user_count = cnt

    # user_login
    for data in user_login_data:
        platform, cnt = data.platform, data.cnt
        obj_dict[platform].user_login = cnt

    # dau
    for data in dau_data:
        platform, cnt = data.platform, data.cnt
        obj_dict[platform].dau = cnt

    # vip_count
    for data in vip_count_data:
        platform, cnt = data.platform, data.cnt
        obj_dict[platform].vip_count = cnt

    # vip_amount
    for data in vip_amount_data:
        platform, cnt = data.platform, data.cnt
        obj_dict[platform].vip_amount = cnt

    # purchase_suc_ratio
    for data in purchase_data:
        platform, suc, fail = data.platform, data.suc, data.fail
        if suc!=None and fail!=None:
            obj_dict[platform].purchase_suc_ratio = div_operation(suc, suc+fail)

    # lc1
    for data in lc1_data:
        platform, cnt = data.platform, data.cnt
        obj_dict[platform].lc1 = cnt

    # lc2
    for data in lc2_data:
        platform, cnt = data.platform, data.cnt
        obj_dict[platform].lc2 = cnt

    # lc3
    for data in lc3_data:
        platform, cnt = data.platform, data.cnt
        obj_dict[platform].lc3 = cnt

    # lc4
    for data in lc4_data:
        platform, cnt = data.platform, data.cnt
        obj_dict[platform].lc4 = cnt

    # lc5
    for data in lc5_data:
        platform, cnt = data.platform, data.cnt
        obj_dict[platform].lc5 = cnt

    # lc6
    for data in lc6_data:
        platform, cnt = data.platform, data.cnt
        obj_dict[platform].lc6 = cnt

    # lc7
    for data in lc7_data:
        platform, cnt = data.platform, data.cnt
        obj_dict[platform].lc7 = cnt

    # lc14
    for data in lc14_data:
        platform, cnt = data.platform, data.cnt
        obj_dict[platform].lc14 = cnt

    # lc30
    for data in lc30_data:
        platform, cnt = data.platform, data.cnt
        obj_dict[platform].lc30 = cnt

    for platform in platform_list:
        obj = obj_dict[platform]
    
    # vip ratio
        if obj.vip_count and obj.dau:
            obj.vip_ratio = div_operation(int(obj.vip_count), int(obj.dau))
    
    # arppu
        if obj.vip_amount and obj.vip_count:
            obj.arppu = div_operation(int(obj.vip_amount), int(obj.vip_count))

    # lc1_ratio
        if obj.lc1 and obj.device_count:
            obj.lc1_ratio = div_operation(int(obj.lc1), int(obj.device_count))

    # lc2_ratio
        if obj.lc2 and obj.device_count:
            obj.lc2_ratio = div_operation(int(obj.lc2), int(obj.device_count))

    # lc3_ratio
        if obj.lc3 and obj.device_count:
            obj.lc3_ratio = div_operation(int(obj.lc3), int(obj.device_count))

    # lc4_ratio
        if obj.lc4 and obj.device_count:
            obj.lc4_ratio = div_operation(int(obj.lc4), int(obj.device_count))

    # lc5_ratio
        if obj.lc5 and obj.device_count:
            obj.lc5_ratio = div_operation(int(obj.lc5), int(obj.device_count))

    # lc6_ratio
        if obj.lc6 and obj.device_count:
            obj.lc6_ratio = div_operation(int(obj.lc6), int(obj.device_count))

    # lc7_ratio
        if obj.lc7 and obj.device_count:
            obj.lc7_ratio = div_operation(int(obj.lc7), int(obj.device_count))

    # lc14_ratio
        if obj.lc14 and obj.device_count:
            obj.lc14_ratio = div_operation(int(obj.lc14), int(obj.device_count))

    # lc30_ratio
        if obj.lc30 and obj.device_count:
            obj.lc30_ratio = div_operation(int(obj.lc30), int(obj.device_count))
    # get_str
        obj.get_str()

    return objs

def get_platform_date_count_objs_list(db, from_date, to_date, platform, desc=False):
    device_count_data = PlatformDeviceCount.objects.using(db).filter(platform=platform, date__range=(from_date, to_date))
    user_count_data = PlatformUserCount.objects.using(db).filter(platform=platform, date__range=(from_date, to_date))
    user_login_data = PlatformUserLogin.objects.using(db).filter(platform=platform, date__range=(from_date, to_date))
    dau_data = PlatformDau.objects.using(db).filter(platform=platform, date__range=(from_date, to_date))
    vip_count_data = PlatformVipCount.objects.using(db).filter(platform=platform, date__range=(from_date, to_date))
    vip_amount_data = PlatformVipAmount.objects.using(db).filter(platform=platform, date__range=(from_date, to_date))
    purchase_data = PlatformPurchase.objects.using(db).filter(platform=platform, date__range=(from_date, to_date))
    lc1_data = PlatformLc1.objects.using(db).filter(platform=platform, date__range=(from_date+datetime.timedelta(days=1), to_date+datetime.timedelta(days=1)))
    lc2_data = PlatformLc2.objects.using(db).filter(platform=platform, date__range=(from_date+datetime.timedelta(days=2), to_date+datetime.timedelta(days=2)))
    lc3_data = PlatformLc3.objects.using(db).filter(platform=platform, date__range=(from_date+datetime.timedelta(days=3), to_date+datetime.timedelta(days=3)))
    lc4_data = PlatformLc4.objects.using(db).filter(platform=platform, date__range=(from_date+datetime.timedelta(days=4), to_date+datetime.timedelta(days=4)))
    lc5_data = PlatformLc5.objects.using(db).filter(platform=platform, date__range=(from_date+datetime.timedelta(days=5), to_date+datetime.timedelta(days=5)))
    lc6_data = PlatformLc6.objects.using(db).filter(platform=platform, date__range=(from_date+datetime.timedelta(days=6), to_date+datetime.timedelta(days=6)))
    lc7_data = PlatformLc7.objects.using(db).filter(platform=platform, date__range=(from_date+datetime.timedelta(days=7), to_date+datetime.timedelta(days=7)))
    lc14_data = PlatformLc14.objects.using(db).filter(platform=platform, date__range=(from_date+datetime.timedelta(days=14), to_date+datetime.timedelta(days=14)))
    lc30_data = PlatformLc30.objects.using(db).filter(platform=platform, date__range=(from_date+datetime.timedelta(days=30), to_date+datetime.timedelta(days=30)))

    objs = []
    obj_dict = {}
    for i in range((to_date - from_date).days + 1):
        the_date = from_date + datetime.timedelta(days=i)
        obj = PlatformCountObject(db, the_date, platform)
        objs.append(obj)
        obj_dict[_get_date_str(the_date)] = obj

    # device_count
    for data in device_count_data:
        date, cnt = data.date, data.cnt
        obj_dict[date].device_count = cnt

    # user_count
    for data in user_count_data:
        date, cnt = data.date, data.cnt
        obj_dict[date].user_count = cnt

    # user_login
    for data in user_login_data:
        date, cnt = data.date, data.cnt
        obj_dict[date].user_login = cnt

    # dau
    for data in dau_data:
        date, cnt = data.date, data.cnt
        obj_dict[date].dau = cnt

    # vip_count
    for data in vip_count_data:
        date, cnt = data.date, data.cnt
        obj_dict[date].vip_count = cnt

    # vip_amount
    for data in vip_amount_data:
        date, cnt = data.date, data.cnt
        obj_dict[date].vip_amount = cnt

    # purchase_suc_ratio
    for data in purchase_data:
        date, suc, fail = data.date, data.suc, data.fail
        if suc!=None and fail!=None:
            obj_dict[date].purchase_suc_ratio = div_operation(suc, suc+fail)

    # lc1
    for data in lc1_data:
        date, cnt = _get_date_str(_get_date_by_str(data.date)-datetime.timedelta(days=1)), data.cnt
        obj_dict[date].lc1 = cnt

    # lc2
    for data in lc2_data:
        date, cnt = _get_date_str(_get_date_by_str(data.date)-datetime.timedelta(days=2)), data.cnt
        obj_dict[date].lc2 = cnt

    # lc3
    for data in lc3_data:
        date, cnt = _get_date_str(_get_date_by_str(data.date)-datetime.timedelta(days=3)), data.cnt
        obj_dict[date].lc3 = cnt

    # lc4
    for data in lc4_data:
        date, cnt = _get_date_str(_get_date_by_str(data.date)-datetime.timedelta(days=4)), data.cnt
        obj_dict[date].lc4 = cnt

    # lc5
    for data in lc5_data:
        date, cnt = _get_date_str(_get_date_by_str(data.date)-datetime.timedelta(days=5)), data.cnt
        obj_dict[date].lc5 = cnt

    # lc6
    for data in lc6_data:
        date, cnt = _get_date_str(_get_date_by_str(data.date)-datetime.timedelta(days=6)), data.cnt
        obj_dict[date].lc6 = cnt

    # lc7
    for data in lc7_data:
        date, cnt = _get_date_str(_get_date_by_str(data.date)-datetime.timedelta(days=7)), data.cnt
        obj_dict[date].lc7 = cnt

    # lc14
    for data in lc14_data:
        date, cnt = _get_date_str(_get_date_by_str(data.date)-datetime.timedelta(days=14)), data.cnt
        obj_dict[date].lc14 = cnt

    # lc30
    for data in lc30_data:
        date, cnt = _get_date_str(_get_date_by_str(data.date)-datetime.timedelta(days=30)), data.cnt
        obj_dict[date].lc30 = cnt

    for i in range((to_date - from_date).days + 1):
        the_date = _get_date_str(from_date + datetime.timedelta(days=i))
        obj = obj_dict[the_date]
    
    # vip ratio
        if obj.vip_count and obj.dau:
            obj.vip_ratio = div_operation(int(obj.vip_count), int(obj.dau))
    
    # arppu
        if obj.vip_amount and obj.vip_count:
            obj.arppu = div_operation(int(obj.vip_amount), int(obj.vip_count))

    # lc1_ratio
        if obj.lc1 and obj.device_count:
            obj.lc1_ratio = div_operation(int(obj.lc1), int(obj.device_count))

    # lc2_ratio
        if obj.lc2 and obj.device_count:
            obj.lc2_ratio = div_operation(int(obj.lc2), int(obj.device_count))

    # lc3_ratio
        if obj.lc3 and obj.device_count:
            obj.lc3_ratio = div_operation(int(obj.lc3), int(obj.device_count))

    # lc4_ratio
        if obj.lc4 and obj.device_count:
            obj.lc4_ratio = div_operation(int(obj.lc4), int(obj.device_count))

    # lc5_ratio
        if obj.lc5 and obj.device_count:
            obj.lc5_ratio = div_operation(int(obj.lc5), int(obj.device_count))

    # lc6_ratio
        if obj.lc6 and obj.device_count:
            obj.lc6_ratio = div_operation(int(obj.lc6), int(obj.device_count))

    # lc7_ratio
        if obj.lc7 and obj.device_count:
            obj.lc7_ratio = div_operation(int(obj.lc7), int(obj.device_count))

    # lc14_ratio
        if obj.lc14 and obj.device_count:
            obj.lc14_ratio = div_operation(int(obj.lc14), int(obj.device_count))

    # lc30_ratio
        if obj.lc30 and obj.device_count:
            obj.lc30_ratio = div_operation(int(obj.lc30), int(obj.device_count))
    # get_str
        obj.get_str()

    if not desc:
        objs.reverse()

    return objs

def get_date_channel_count_objs_list(db, date, channel_list):
    device_count_data = ChannelDeviceCount.objects.using(db).filter(date=date, channel_id__in=channel_list)
    user_count_data = ChannelUserCount.objects.using(db).filter(date=date, channel_id__in=channel_list)
    user_login_data = ChannelUserLogin.objects.using(db).filter(date=date, channel_id__in=channel_list)
    dau_data = ChannelDau.objects.using(db).filter(date=date, channel_id__in=channel_list)
    vip_count_data = ChannelVipCount.objects.using(db).filter(date=date, channel_id__in=channel_list)
    vip_amount_data = ChannelVipAmount.objects.using(db).filter(date=date, channel_id__in=channel_list)
    purchase_data = ChannelPurchase.objects.using(db).filter(date=date, channel_id__in=channel_list)
    lc1_data = ChannelLc1.objects.using(db).filter(date=date+datetime.timedelta(days=1), channel_id__in=channel_list)
    lc2_data = ChannelLc2.objects.using(db).filter(date=date+datetime.timedelta(days=2), channel_id__in=channel_list)
    lc3_data = ChannelLc3.objects.using(db).filter(date=date+datetime.timedelta(days=3), channel_id__in=channel_list)
    lc4_data = ChannelLc4.objects.using(db).filter(date=date+datetime.timedelta(days=4), channel_id__in=channel_list)
    lc5_data = ChannelLc5.objects.using(db).filter(date=date+datetime.timedelta(days=5), channel_id__in=channel_list)
    lc6_data = ChannelLc6.objects.using(db).filter(date=date+datetime.timedelta(days=6), channel_id__in=channel_list)
    lc7_data = ChannelLc7.objects.using(db).filter(date=date+datetime.timedelta(days=7), channel_id__in=channel_list)
    lc14_data = ChannelLc14.objects.using(db).filter(date=date+datetime.timedelta(days=14), channel_id__in=channel_list)
    lc30_data = ChannelLc30.objects.using(db).filter(date=date+datetime.timedelta(days=30), channel_id__in=channel_list)

    objs = []
    obj_dict = {}
    for channel in channel_list:
        obj = ChannelCountObject(db, date, channel)
        objs.append(obj)
        obj_dict[channel] = obj

    # device_count
    for data in device_count_data:
        channel, cnt = data.channel_id, data.cnt
        obj_dict[channel].device_count = cnt

    # user_count
    for data in user_count_data:
        channel, cnt = data.channel_id, data.cnt
        obj_dict[channel].user_count = cnt

    # user_login
    for data in user_login_data:
        channel, cnt = data.channel_id, data.cnt
        obj_dict[channel].user_login = cnt

    # dau
    for data in dau_data:
        channel, cnt = data.channel_id, data.cnt
        obj_dict[channel].dau = cnt

    # vip_count
    for data in vip_count_data:
        channel, cnt = data.channel_id, data.cnt
        obj_dict[channel].vip_count = cnt

    # vip_amount
    for data in vip_amount_data:
        channel, cnt = data.channel_id, data.cnt
        obj_dict[channel].vip_amount = cnt

    # purchase_suc_ratio
    for data in purchase_data:
        channel, suc, fail = data.channel_id, data.suc, data.fail
        if suc!=None and fail!=None:
            obj_dict[channel].purchase_suc_ratio = div_operation(suc, suc+fail)

    # lc1
    for data in lc1_data:
        channel, cnt = data.channel_id, data.cnt
        obj_dict[channel].lc1 = cnt

    # lc2
    for data in lc2_data:
        channel, cnt = data.channel_id, data.cnt
        obj_dict[channel].lc2 = cnt

    # lc3
    for data in lc3_data:
        channel, cnt = data.channel_id, data.cnt
        obj_dict[channel].lc3 = cnt

    # lc4
    for data in lc4_data:
        channel, cnt = data.channel_id, data.cnt
        obj_dict[channel].lc4 = cnt

    # lc5
    for data in lc5_data:
        channel, cnt = data.channel_id, data.cnt
        obj_dict[channel].lc5 = cnt

    # lc6
    for data in lc6_data:
        channel, cnt = data.channel_id, data.cnt
        obj_dict[channel].lc6 = cnt

    # lc7
    for data in lc7_data:
        channel, cnt = data.channel_id, data.cnt
        obj_dict[channel].lc7 = cnt

    # lc14
    for data in lc14_data:
        channel, cnt = data.channel_id, data.cnt
        obj_dict[channel].lc14 = cnt

    # lc30
    for data in lc30_data:
        channel, cnt = data.channel_id, data.cnt
        obj_dict[channel].lc30 = cnt

    for channel in channel_list:
        obj = obj_dict[channel]
    
    # vip ratio
        if obj.vip_count and obj.dau:
            obj.vip_ratio = div_operation(int(obj.vip_count), int(obj.dau))
    
    # arppu
        if obj.vip_amount and obj.vip_count:
            obj.arppu = div_operation(int(obj.vip_amount), int(obj.vip_count))

    # lc1_ratio
        if obj.lc1 and obj.device_count:
            obj.lc1_ratio = div_operation(int(obj.lc1), int(obj.device_count))

    # lc2_ratio
        if obj.lc2 and obj.device_count:
            obj.lc2_ratio = div_operation(int(obj.lc2), int(obj.device_count))

    # lc3_ratio
        if obj.lc3 and obj.device_count:
            obj.lc3_ratio = div_operation(int(obj.lc3), int(obj.device_count))

    # lc4_ratio
        if obj.lc4 and obj.device_count:
            obj.lc4_ratio = div_operation(int(obj.lc4), int(obj.device_count))

    # lc5_ratio
        if obj.lc5 and obj.device_count:
            obj.lc5_ratio = div_operation(int(obj.lc5), int(obj.device_count))

    # lc6_ratio
        if obj.lc6 and obj.device_count:
            obj.lc6_ratio = div_operation(int(obj.lc6), int(obj.device_count))

    # lc7_ratio
        if obj.lc7 and obj.device_count:
            obj.lc7_ratio = div_operation(int(obj.lc7), int(obj.device_count))

    # lc14_ratio
        if obj.lc14 and obj.device_count:
            obj.lc14_ratio = div_operation(int(obj.lc14), int(obj.device_count))

    # lc30_ratio
        if obj.lc30 and obj.device_count:
            obj.lc30_ratio = div_operation(int(obj.lc30), int(obj.device_count))
    # get_str
        obj.get_str()

    return objs

def get_channel_date_count_objs_list(db, from_date, to_date, channel, desc=False):
    device_count_data = ChannelDeviceCount.objects.using(db).filter(channel_id=channel, date__range=(from_date, to_date))
    user_count_data = ChannelUserCount.objects.using(db).filter(channel_id=channel, date__range=(from_date, to_date))
    user_login_data = ChannelUserLogin.objects.using(db).filter(channel_id=channel, date__range=(from_date, to_date))
    dau_data = ChannelDau.objects.using(db).filter(channel_id=channel, date__range=(from_date, to_date))
    vip_count_data = ChannelVipCount.objects.using(db).filter(channel_id=channel, date__range=(from_date, to_date))
    vip_amount_data = ChannelVipAmount.objects.using(db).filter(channel_id=channel, date__range=(from_date, to_date))
    purchase_data = ChannelPurchase.objects.using(db).filter(channel_id=channel, date__range=(from_date, to_date))
    lc1_data = ChannelLc1.objects.using(db).filter(channel_id=channel, date__range=(from_date+datetime.timedelta(days=1), to_date+datetime.timedelta(days=1)))
    lc2_data = ChannelLc2.objects.using(db).filter(channel_id=channel, date__range=(from_date+datetime.timedelta(days=2), to_date+datetime.timedelta(days=2)))
    lc3_data = ChannelLc3.objects.using(db).filter(channel_id=channel, date__range=(from_date+datetime.timedelta(days=3), to_date+datetime.timedelta(days=3)))
    lc4_data = ChannelLc4.objects.using(db).filter(channel_id=channel, date__range=(from_date+datetime.timedelta(days=4), to_date+datetime.timedelta(days=4)))
    lc5_data = ChannelLc5.objects.using(db).filter(channel_id=channel, date__range=(from_date+datetime.timedelta(days=5), to_date+datetime.timedelta(days=5)))
    lc6_data = ChannelLc6.objects.using(db).filter(channel_id=channel, date__range=(from_date+datetime.timedelta(days=6), to_date+datetime.timedelta(days=6)))
    lc7_data = ChannelLc7.objects.using(db).filter(channel_id=channel, date__range=(from_date+datetime.timedelta(days=7), to_date+datetime.timedelta(days=7)))
    lc14_data = ChannelLc14.objects.using(db).filter(channel_id=channel, date__range=(from_date+datetime.timedelta(days=14), to_date+datetime.timedelta(days=14)))
    lc30_data = ChannelLc30.objects.using(db).filter(channel_id=channel, date__range=(from_date+datetime.timedelta(days=30), to_date+datetime.timedelta(days=30)))

    objs = []
    obj_dict = {}
    for i in range((to_date - from_date).days + 1):
        the_date = from_date + datetime.timedelta(days=i)
        obj = ChannelCountObject(db, the_date, channel)
        objs.append(obj)
        obj_dict[_get_date_str(the_date)] = obj

    # device_count
    for data in device_count_data:
        date, cnt = data.date, data.cnt
        obj_dict[date].device_count = cnt

    # user_count
    for data in user_count_data:
        date, cnt = data.date, data.cnt
        obj_dict[date].user_count = cnt

    # user_login
    for data in user_login_data:
        date, cnt = data.date, data.cnt
        obj_dict[date].user_login = cnt

    # dau
    for data in dau_data:
        date, cnt = data.date, data.cnt
        obj_dict[date].dau = cnt

    # vip_count
    for data in vip_count_data:
        date, cnt = data.date, data.cnt
        obj_dict[date].vip_count = cnt

    # vip_amount
    for data in vip_amount_data:
        date, cnt = data.date, data.cnt
        obj_dict[date].vip_amount = cnt

    # purchase_suc_ratio
    for data in purchase_data:
        date, suc, fail = data.date, data.suc, data.fail
        if suc!=None and fail!=None:
            obj_dict[date].purchase_suc_ratio = div_operation(suc, suc+fail)

    # lc1
    for data in lc1_data:
        date, cnt = _get_date_str(_get_date_by_str(data.date)-datetime.timedelta(days=1)), data.cnt
        obj_dict[date].lc1 = cnt

    # lc2
    for data in lc2_data:
        date, cnt = _get_date_str(_get_date_by_str(data.date)-datetime.timedelta(days=2)), data.cnt
        obj_dict[date].lc2 = cnt

    # lc3
    for data in lc3_data:
        date, cnt = _get_date_str(_get_date_by_str(data.date)-datetime.timedelta(days=3)), data.cnt
        obj_dict[date].lc3 = cnt

    # lc4
    for data in lc4_data:
        date, cnt = _get_date_str(_get_date_by_str(data.date)-datetime.timedelta(days=4)), data.cnt
        obj_dict[date].lc4 = cnt

    # lc5
    for data in lc5_data:
        date, cnt = _get_date_str(_get_date_by_str(data.date)-datetime.timedelta(days=5)), data.cnt
        obj_dict[date].lc5 = cnt

    # lc6
    for data in lc6_data:
        date, cnt = _get_date_str(_get_date_by_str(data.date)-datetime.timedelta(days=6)), data.cnt
        obj_dict[date].lc6 = cnt

    # lc7
    for data in lc7_data:
        date, cnt = _get_date_str(_get_date_by_str(data.date)-datetime.timedelta(days=7)), data.cnt
        obj_dict[date].lc7 = cnt

    # lc14
    for data in lc14_data:
        date, cnt = _get_date_str(_get_date_by_str(data.date)-datetime.timedelta(days=14)), data.cnt
        obj_dict[date].lc14 = cnt

    # lc30
    for data in lc30_data:
        date, cnt = _get_date_str(_get_date_by_str(data.date)-datetime.timedelta(days=30)), data.cnt
        obj_dict[date].lc30 = cnt

    for i in range((to_date - from_date).days + 1):
        the_date = _get_date_str(from_date + datetime.timedelta(days=i))
        obj = obj_dict[the_date]
    
    # vip ratio
        if obj.vip_count and obj.dau:
            obj.vip_ratio = div_operation(int(obj.vip_count), int(obj.dau))
    
    # arppu
        if obj.vip_amount and obj.vip_count:
            obj.arppu = div_operation(int(obj.vip_amount), int(obj.vip_count))

    # lc1_ratio
        if obj.lc1 and obj.device_count:
            obj.lc1_ratio = div_operation(int(obj.lc1), int(obj.device_count))

    # lc2_ratio
        if obj.lc2 and obj.device_count:
            obj.lc2_ratio = div_operation(int(obj.lc2), int(obj.device_count))

    # lc3_ratio
        if obj.lc3 and obj.device_count:
            obj.lc3_ratio = div_operation(int(obj.lc3), int(obj.device_count))

    # lc4_ratio
        if obj.lc4 and obj.device_count:
            obj.lc4_ratio = div_operation(int(obj.lc4), int(obj.device_count))

    # lc5_ratio
        if obj.lc5 and obj.device_count:
            obj.lc5_ratio = div_operation(int(obj.lc5), int(obj.device_count))

    # lc6_ratio
        if obj.lc6 and obj.device_count:
            obj.lc6_ratio = div_operation(int(obj.lc6), int(obj.device_count))

    # lc7_ratio
        if obj.lc7 and obj.device_count:
            obj.lc7_ratio = div_operation(int(obj.lc7), int(obj.device_count))

    # lc14_ratio
        if obj.lc14 and obj.device_count:
            obj.lc14_ratio = div_operation(int(obj.lc14), int(obj.device_count))

    # lc30_ratio
        if obj.lc30 and obj.device_count:
            obj.lc30_ratio = div_operation(int(obj.lc30), int(obj.device_count))
    # get_str
        obj.get_str()

    if not desc:
        objs.reverse()

    return objs
    