# -*- coding: utf-8 -*-
import datetime

from django.conf import settings

from gna.tabulate.models import (
    TopVip,
    TopDia,
    TopZel,
    TopKarma,
    Vip7,
    BrvUserInfo,
    BrvUserTeamInfo,
)
from gna.common import (
    div_operation,
)

##### str #####
def _get_date_str(date):
    if type(date)==datetime.date or type(date)==datetime.datetime:
        return date.strftime('%Y-%m-%d')
    return date

def _get_date_by_str(date_str):
    return datetime.datetime.strptime(date_str, '%Y-%m-%d')

def _get_str_by_int(value):
    if value != None:
        return str(int(value))
    else:
        return None

def _get_str_by_float(value):
    if value != None:
        return '%.1f' % (value)
    else:
        return None

def _get_percent_by_float(value):
    if value:
        return '%.1f%%' % (value*100.0)
    else:
        return None

def _get_str_by_datetime(value):
    if value:
        return str(value)
    else:
        return None

def _get_str_by_date(value):
    if value:
        return str(value)
    else:
        return None

def _get_update_day(dt):
    return (datetime.date.today() - dt.date()).days

##### api #####

# 当日充值排行榜
class TopVipObject(object):
    user_str = None
    lv = None
    update_date = None
    update_day = None
    rank = None
    rank_srt = None

    def __init__(self, date, platform, zone, user_id, channel_id, amount, times):
        self.date = date
        self.platform = platform
        self.zone = zone
        self.user_id = user_id
        self.channel_id = str(channel_id)
        self.amount = amount
        self.times = times

    def get_str(self):
        self.date_str = _get_date_str(self.date)
        self.platform_str = _get_str_by_int(self.platform)
        self.zone_str = settings.TABULATE_ZONE_NAME[self.zone]
        if self.channel_id in settings.TABULATE_CHANNEL_NAME:
            self.channel_str = settings.TABULATE_CHANNEL_NAME[self.channel_id]
        else:
            self.channel_str = _get_str_by_int(self.channel_id)
        self.amount_str = _get_str_by_int(self.amount)
        self.times_str = _get_str_by_int(self.times)

        self.lv_str = _get_str_by_int(self.lv)
        self.update_date_str = _get_str_by_datetime(self.update_date)
        self.update_day_str = _get_str_by_int(self.update_day)

def get_top_vip_objs_list(db, date):
    zone_user_info_cache = {}

    query_data = TopVip.objects.using(db).filter(date=date)

    objs = []
    for data in query_data:
        date, platform, zone, user_id, channel_id, amount, times = data.date, data.platform, data.zone, data.user_id, data.channel_id, data.amount, data.times
        if not amount:
            continue
        obj = TopVipObject(date, platform, zone, user_id, channel_id, amount, times)

        if zone not in zone_user_info_cache:
            zone_user_info_cache[zone] = {}
            user_info_db = zone + '_brave_cn_common'

            user_query_data = BrvUserInfo.objects.using(user_info_db).values_list('USER_ID', 'HANDLE_NAME')
            for user_data in user_query_data:
                uid, name = user_data
                zone_user_info_cache[zone][uid] = {'handle_name':name, 'lv':None, 'update_date':None}

            user_team_query_data = BrvUserTeamInfo.objects.using(user_info_db).values_list('USER_ID', 'LV', 'UPDATEDATE')
            for user_team_data in user_team_query_data:
                uid, lv, updatedate = user_team_data
                if uid in zone_user_info_cache[zone]:
                    zone_user_info_cache[zone][uid].update({'lv':lv, 'update_date':updatedate})
                else:
                    zone_user_info_cache[zone][uid] = {'lv':lv, 'update_date':updatedate, 'handle_name':None}

        user_info = zone_user_info_cache[zone][user_id]
        handle_name, update_date, lv = user_info['handle_name'], user_info['update_date'], user_info['lv']
        obj.user_str = handle_name
        obj.update_date = update_date
        obj.lv = lv
        obj.update_day = _get_update_day(update_date)
        obj.get_str()
        objs.append(obj)

    objs.sort(key=lambda x: x.amount, reverse=True)

    rank = 1
    for obj in objs:
        obj.rank = rank
        obj.rank_str = str(rank)
        rank += 1

    return objs

# 钻石排行榜(do_type:1产出,2消耗)
class TopResourceObject(object):
    user_str = None
    rank = None
    rank_srt = None

    def __init__(self, date, platform, zone, user_id, channel_id, amount, times):
        self.date = date
        self.platform = platform
        self.zone = zone
        self.user_id = user_id
        self.channel_id = str(channel_id)
        self.amount = amount
        self.times = times

    def get_str(self):
        self.date_str = _get_date_str(self.date)
        self.platform_str = _get_str_by_int(self.platform)
        self.zone_str = settings.TABULATE_ZONE_NAME[self.zone]
        if self.channel_id in settings.TABULATE_CHANNEL_NAME:
            self.channel_str = settings.TABULATE_CHANNEL_NAME[self.channel_id]
        else:
            self.channel_str = _get_str_by_int(self.channel_id)
        self.amount_str = _get_str_by_int(self.amount)
        self.times_str = _get_str_by_int(self.times)


def get_top_dia_objs_list(db, date, do_type):
    zone_user_info_cache = {}

    query_data = TopDia.objects.using(db).filter(date=date, do_type=do_type)

    objs = []
    for data in query_data:
        date, platform, zone, user_id, channel_id, amount, times = data.date, data.platform, data.zone, data.user_id, data.channel_id, data.amount, data.times
        if not amount:
            continue
        obj = TopResourceObject(date, platform, zone, user_id, channel_id, amount, times)

        if zone not in zone_user_info_cache:
            zone_user_info_cache[zone] = {}
            user_info_db = zone + '_brave_cn_common'

            user_query_data = BrvUserInfo.objects.using(user_info_db).values_list('USER_ID', 'HANDLE_NAME')
            for user_data in user_query_data:
                uid, name = user_data
                zone_user_info_cache[zone][uid] = {'handle_name':name}

        user_info = zone_user_info_cache[zone][user_id]
        handle_name = user_info['handle_name']
        obj.user_str = handle_name
        obj.get_str()
        objs.append(obj)

    objs.sort(key=lambda x: x.amount, reverse=True)

    rank = 1
    for obj in objs:
        obj.rank = rank
        obj.rank_str = str(rank)
        rank += 1

    return objs

# 金币排行榜(do_type:1产出,2消耗)
def get_top_zel_objs_list(db, date, do_type):
    zone_user_info_cache = {}

    query_data = TopZel.objects.using(db).filter(date=date, do_type=do_type)

    objs = []
    for data in query_data:
        date, platform, zone, user_id, channel_id, amount, times = data.date, data.platform, data.zone, data.user_id, data.channel_id, data.amount, data.times
        if not amount:
            continue
        obj = TopResourceObject(date, platform, zone, user_id, channel_id, amount, times)

        if zone not in zone_user_info_cache:
            zone_user_info_cache[zone] = {}
            user_info_db = zone + '_brave_cn_common'

            user_query_data = BrvUserInfo.objects.using(user_info_db).values_list('USER_ID', 'HANDLE_NAME')
            for user_data in user_query_data:
                uid, name = user_data
                zone_user_info_cache[zone][uid] = {'handle_name':name}

        user_info = zone_user_info_cache[zone][user_id]
        handle_name = user_info['handle_name']
        obj.user_str = handle_name
        obj.get_str()
        objs.append(obj)

    objs.sort(key=lambda x: x.amount, reverse=True)

    rank = 1
    for obj in objs:
        obj.rank = rank
        obj.rank_str = str(rank)
        rank += 1

    return objs

# 魂排行榜(do_type:1产出,2消耗)
def get_top_karma_objs_list(db, date, do_type):
    zone_user_info_cache = {}

    query_data = TopKarma.objects.using(db).filter(date=date, do_type=do_type)

    objs = []
    for data in query_data:
        date, platform, zone, user_id, channel_id, amount, times = data.date, data.platform, data.zone, data.user_id, data.channel_id, data.amount, data.times
        if not amount:
            continue
        obj = TopResourceObject(date, platform, zone, user_id, channel_id, amount, times)

        if zone not in zone_user_info_cache:
            zone_user_info_cache[zone] = {}
            user_info_db = zone + '_brave_cn_common'

            user_query_data = BrvUserInfo.objects.using(user_info_db).values_list('USER_ID', 'HANDLE_NAME')
            for user_data in user_query_data:
                uid, name = user_data
                zone_user_info_cache[zone][uid] = {'handle_name':name}

        user_info = zone_user_info_cache[zone][user_id]
        handle_name = user_info['handle_name']
        obj.user_str = handle_name
        obj.get_str()
        objs.append(obj)

    objs.sort(key=lambda x: x.amount, reverse=True)

    rank = 1
    for obj in objs:
        obj.rank = rank
        obj.rank_str = str(rank)
        rank += 1

    return objs

# 充值用户流失预警排行榜
class TopVip7Object(object):
    user_str = None
    lv = None
    update_date = None
    user_type = None
    user_type_str = None
    rank = None
    rank_srt = None

    def __init__(self, zone, user_id, channel_id, platform, amount7, amount3):
        self.zone = zone
        self.user_id = user_id
        self.channel_id = str(channel_id)
        self.platform = platform
        self.amount7 = amount7
        self.amount3 = amount3

    def get_str(self):
        self.zone_str = settings.TABULATE_ZONE_NAME[self.zone]
        if self.channel_id in settings.TABULATE_CHANNEL_NAME:
            self.channel_str = settings.TABULATE_CHANNEL_NAME[self.channel_id]
        else:
            self.channel_str = _get_str_by_int(self.channel_id)
        self.platform_str = _get_str_by_int(self.platform)
        self.amount7_str = _get_str_by_int(self.amount7)
        self.amount3_str = _get_str_by_int(self.amount3)

        self.lv_str = _get_str_by_int(self.lv)
        self.update_date_str = _get_str_by_date(self.update_date)

def get_top_vip7_objs_list(db):
    zone_user_info_cache = {}

    query_data = Vip7.objects.using(db).all()

    objs = []
    for data in query_data:
        zone, user_id, channel_id, platform, amount7, amount3 = data.zone, data.user_id, data.channel_id, data.platform, data.amount7, data.amount3
        obj = TopVip7Object(zone, user_id, channel_id, platform, amount7, amount3)

        if zone not in zone_user_info_cache:
            zone_user_info_cache[zone] = {}
            user_info_db = zone + '_brave_cn_common'

            user_query_data = BrvUserInfo.objects.using(user_info_db).values_list('USER_ID', 'HANDLE_NAME')
            for user_data in user_query_data:
                uid, name = user_data
                zone_user_info_cache[zone][uid] = {'handle_name':name, 'lv':None, 'update_date':None}

            user_team_query_data = BrvUserTeamInfo.objects.using(user_info_db).values_list('USER_ID', 'LV', 'UPDATEDATE')
            for user_team_data in user_team_query_data:
                uid, lv, updatedate = user_team_data
                if uid in zone_user_info_cache[zone]:
                    zone_user_info_cache[zone][uid].update({'lv':lv, 'update_date':updatedate})
                else:
                    zone_user_info_cache[zone][uid] = {'lv':lv, 'update_date':updatedate, 'handle_name':None}

        user_info = zone_user_info_cache[zone][user_id]
        handle_name, update_date, lv = user_info['handle_name'], user_info['update_date'], user_info['lv']
        obj.user_str = handle_name
        obj.update_date = update_date.date()
        obj.lv = lv
        if _get_update_day(update_date) > 3:
            obj.user_type = 0
            obj.user_type_str = '潜在流失'
        else:
            obj.user_type = 1
            obj.user_type_str = '活跃用户'
        obj.get_str()
        objs.append(obj)

    objs.sort(key=lambda x: (x.user_type, -x.amount7))

    rank = 1
    for obj in objs:
        obj.rank = rank
        obj.rank_str = str(rank)
        rank += 1

    return objs






