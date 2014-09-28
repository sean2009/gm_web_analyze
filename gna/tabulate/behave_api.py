# -*- coding: utf-8 -*-
import datetime

from django.conf import settings

from gna.tabulate.models import (
    PaymentLevel,
    ZelInc,
    ZelDec,
    DiaInc,
    DiaDec,
    KarmaInc,
    KarmaDec,
    NewUserLevel,
    ArenaChallenge,
    DungeonKey,
    UnitEvo,
    UnitMix,
    UnitSell,
    FacilityLvup,
    LocationLvup,
    BmRefresh,
    BmBuy,
    BmGoods,
    BrvItemMst,
    BrvUnitMst,
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

##### api #####

# 当日创角等级分布
class NewUserLevelObject(object):
    percent = None
    total_percent = None

    def __init__(self, date, zone, lv, count):
        self.date = date
        self.zone = zone
        self.lv = lv
        self.count = count

    def get_str(self):
        self.date_str = _get_date_str(self.date)
        self.zone_str = settings.TABULATE_ZONE_NAME[self.zone]
        self.lv_str = _get_str_by_int(self.lv)
        self.count_str = _get_str_by_int(self.count)
        self.percent_str = _get_percent_by_float(self.percent)
        self.total_percent_str = _get_percent_by_float(self.total_percent)

def get_new_user_level_objs_list(db, date, zone):
    query_data = NewUserLevel.objects.using(db).filter(date=date, zone=zone)

    objs = []
    all_count = 0
    for data in query_data:
        lv, count = data.lv, data.count
        obj = NewUserLevelObject(date, zone, lv, count)
        all_count += count
        objs.append(obj)

    objs.sort(key=lambda x: x.lv)

    total = 0
    for obj in objs:
        obj.percent = div_operation(obj.count, all_count)
        total += obj.count
        obj.total_percent = div_operation(total, all_count)
        obj.get_str()

    return objs

def get_new_user_level_summary_objs_list(db, date):
    query_data = NewUserLevel.objects.using(db).filter(date=date)

    objs = []
    obj_dict = {}
    all_count = 0
    for data in query_data:
        lv, count = data.lv, data.count
        if lv in obj_dict:
            obj_dict[lv].count += count
        else:
            obj = NewUserLevelObject(date, 'summary', lv, count)
            objs.append(obj)
            obj_dict[lv] = obj
        all_count += count

    objs.sort(key=lambda x: x.lv)

    total = 0
    for obj in objs:
        obj.percent = div_operation(obj.count, all_count)
        total += obj.count
        obj.total_percent = div_operation(total, all_count)
        obj.get_str()

    return objs

# 充值档次
class PaymentLevelObject(object):
    def __init__(self, date, platform, zone, purchase_id, user_count, times_count, amount):
        self.date = date
        self.zone = zone
        self.platform = platform
        self.purchase_id = purchase_id
        self.user_count = user_count
        self.times_count = times_count
        self.amount = amount  

    def get_str(self):
        self.date_str = _get_date_str(self.date)
        self.zone_str = settings.TABULATE_ZONE_NAME[self.zone]
        self.platform_str = _get_str_by_int(self.platform)
        self.purchase_id_str = settings.TABULATE_PURCHASE_ID_NAME[self.purchase_id]
        self.user_count_str = _get_str_by_int(self.user_count)
        self.times_count_str = _get_str_by_int(self.times_count)
        self.amount_str = _get_str_by_int(self.amount)

def get_payment_level_objs_list(db, date, zone):
    query_data = PaymentLevel.objects.using(db).filter(date=date, zone=zone)

    objs = []
    for data in query_data:
        platform, purchase_id, user_count, times_count, amount = data.platform, data.purchase_id, data.user_count, data.times_count, data.amount
        obj = PaymentLevelObject(date, platform, zone, purchase_id, user_count, times_count, amount)
        obj.get_str()
        objs.append(obj)

    objs.sort(key=lambda x: x.purchase_id)

    return objs

def get_payment_level_summary_objs_list(db, date):
    zone = 'summary'
    query_data = PaymentLevel.objects.using(db).filter(date=date)

    objs = []
    obj_dict = {}
    for data in query_data:
        platform, purchase_id, user_count, times_count, amount = data.platform, data.purchase_id, data.user_count, data.times_count, data.amount
        if purchase_id in obj_dict:
            obj = obj_dict[purchase_id]
            obj.user_count += user_count
            obj.times_count += times_count
            obj.amount += amount
        else:
            obj = PaymentLevelObject(date, platform, zone, purchase_id, user_count, times_count, amount)
            objs.append(obj)
            obj_dict[purchase_id] = obj

    objs.sort(key=lambda x: x.purchase_id)        

    for obj in objs:
        obj.get_str()

    return objs

# 金币产出
class ResourceObject(object):
    def __init__(self, date, platform, zone, channel_id, user_count, times_count, amount):
        self.date = date
        self.zone = zone
        self.platform = platform
        self.channel_id = channel_id
        self.user_count = user_count
        self.times_count = times_count
        self.amount = amount  

    def get_str(self):
        self.date_str = _get_date_str(self.date)
        self.zone_str = settings.TABULATE_ZONE_NAME[self.zone]
        self.platform_str = _get_str_by_int(self.platform)
        if self.channel_id in settings.TABULATE_RESOURCE_CHANNEL_ID_NAME:
            self.channel_id_str = settings.TABULATE_RESOURCE_CHANNEL_ID_NAME[self.channel_id]
        else:
            self.channel_id_str = str(self.channel_id)
        self.user_count_str = _get_str_by_int(self.user_count)
        self.times_count_str = _get_str_by_int(self.times_count)
        self.amount_str = _get_str_by_int(self.amount)

def get_zel_inc_objs_list(db, date, zone):
    query_data = ZelInc.objects.using(db).filter(date=date, zone=zone)

    objs = []
    for data in query_data:
        platform, channel_id, user_count, times_count, amount = data.platform, data.channel_id, data.user_count, data.times_count, data.amount
        obj = ResourceObject(date, platform, zone, channel_id, user_count, times_count, amount)
        obj.get_str()
        objs.append(obj)

    objs.sort(key=lambda x: x.channel_id)

    return objs

def get_zel_inc_summary_objs_list(db, date):
    zone = 'summary'
    query_data = ZelInc.objects.using(db).filter(date=date)

    objs = []
    obj_dict = {}
    for data in query_data:
        platform, channel_id, user_count, times_count, amount = data.platform, data.channel_id, data.user_count, data.times_count, data.amount
        if channel_id in obj_dict:
            obj = obj_dict[channel_id]
            obj.user_count += user_count
            obj.times_count += times_count
            obj.amount += amount
        else:
            obj = ResourceObject(date, platform, zone, channel_id, user_count, times_count, amount)
            objs.append(obj)
            obj_dict[channel_id] = obj

    objs.sort(key=lambda x: x.channel_id)

    for obj in objs:
        obj.get_str()

    return objs

# 金币消耗
def get_zel_dec_objs_list(db, date, zone):
    query_data = ZelDec.objects.using(db).filter(date=date, zone=zone)

    objs = []
    for data in query_data:
        platform, channel_id, user_count, times_count, amount = data.platform, data.channel_id, data.user_count, data.times_count, data.amount
        obj = ResourceObject(date, platform, zone, channel_id, user_count, times_count, amount)
        obj.get_str()
        objs.append(obj)

    objs.sort(key=lambda x: x.channel_id)

    return objs

def get_zel_dec_summary_objs_list(db, date):
    zone = 'summary'
    query_data = ZelDec.objects.using(db).filter(date=date)

    objs = []
    obj_dict = {}
    for data in query_data:
        platform, channel_id, user_count, times_count, amount = data.platform, data.channel_id, data.user_count, data.times_count, data.amount
        if channel_id in obj_dict:
            obj = obj_dict[channel_id]
            obj.user_count += user_count
            obj.times_count += times_count
            obj.amount += amount
        else:
            obj = ResourceObject(date, platform, zone, channel_id, user_count, times_count, amount)
            objs.append(obj)
            obj_dict[channel_id] = obj

    objs.sort(key=lambda x: x.channel_id)

    for obj in objs:
        obj.get_str()

    return objs

# 钻石产出
def get_dia_inc_objs_list(db, date, zone):
    query_data = DiaInc.objects.using(db).filter(date=date, zone=zone)

    objs = []
    for data in query_data:
        platform, channel_id, user_count, times_count, amount = data.platform, data.channel_id, data.user_count, data.times_count, data.amount
        obj = ResourceObject(date, platform, zone, channel_id, user_count, times_count, amount)
        obj.get_str()
        objs.append(obj)

    objs.sort(key=lambda x: x.channel_id)

    return objs

def get_dia_inc_summary_objs_list(db, date):
    zone = 'summary'
    query_data = DiaInc.objects.using(db).filter(date=date)

    objs = []
    obj_dict = {}
    for data in query_data:
        platform, channel_id, user_count, times_count, amount = data.platform, data.channel_id, data.user_count, data.times_count, data.amount
        if channel_id in obj_dict:
            obj = obj_dict[channel_id]
            obj.user_count += user_count
            obj.times_count += times_count
            obj.amount += amount
        else:
            obj = ResourceObject(date, platform, zone, channel_id, user_count, times_count, amount)
            objs.append(obj)
            obj_dict[channel_id] = obj

    objs.sort(key=lambda x: x.channel_id)

    for obj in objs:
        obj.get_str()

    return objs

# 钻石消耗
def get_dia_dec_objs_list(db, date, zone):
    query_data = DiaDec.objects.using(db).filter(date=date, zone=zone)

    objs = []
    for data in query_data:
        platform, channel_id, user_count, times_count, amount = data.platform, data.channel_id, data.user_count, data.times_count, data.amount
        obj = ResourceObject(date, platform, zone, channel_id, user_count, times_count, amount)
        obj.get_str()
        objs.append(obj)

    objs.sort(key=lambda x: x.channel_id)

    return objs

def get_dia_dec_summary_objs_list(db, date):
    zone = 'summary'
    query_data = DiaDec.objects.using(db).filter(date=date)

    objs = []
    obj_dict = {}
    for data in query_data:
        platform, channel_id, user_count, times_count, amount = data.platform, data.channel_id, data.user_count, data.times_count, data.amount
        if channel_id in obj_dict:
            obj = obj_dict[channel_id]
            obj.user_count += user_count
            obj.times_count += times_count
            obj.amount += amount
        else:
            obj = ResourceObject(date, platform, zone, channel_id, user_count, times_count, amount)
            objs.append(obj)
            obj_dict[channel_id] = obj

    objs.sort(key=lambda x: x.channel_id)

    for obj in objs:
        obj.get_str()

    return objs

# 魂产出
def get_karma_inc_objs_list(db, date, zone):
    query_data = KarmaInc.objects.using(db).filter(date=date, zone=zone)

    objs = []
    for data in query_data:
        platform, channel_id, user_count, times_count, amount = data.platform, data.channel_id, data.user_count, data.times_count, data.amount
        obj = ResourceObject(date, platform, zone, channel_id, user_count, times_count, amount)
        obj.get_str()
        objs.append(obj)

    objs.sort(key=lambda x: x.channel_id)

    return objs

def get_karma_inc_summary_objs_list(db, date):
    zone = 'summary'
    query_data = KarmaInc.objects.using(db).filter(date=date)

    objs = []
    obj_dict = {}
    for data in query_data:
        platform, channel_id, user_count, times_count, amount = data.platform, data.channel_id, data.user_count, data.times_count, data.amount
        if channel_id in obj_dict:
            obj = obj_dict[channel_id]
            obj.user_count += user_count
            obj.times_count += times_count
            obj.amount += amount
        else:
            obj = ResourceObject(date, platform, zone, channel_id, user_count, times_count, amount)
            objs.append(obj)
            obj_dict[channel_id] = obj

    objs.sort(key=lambda x: x.channel_id)

    for obj in objs:
        obj.get_str()

    return objs

# 魂消耗
def get_karma_dec_objs_list(db, date, zone):
    query_data = KarmaDec.objects.using(db).filter(date=date, zone=zone)

    objs = []
    for data in query_data:
        platform, channel_id, user_count, times_count, amount = data.platform, data.channel_id, data.user_count, data.times_count, data.amount
        obj = ResourceObject(date, platform, zone, channel_id, user_count, times_count, amount)
        obj.get_str()
        objs.append(obj)

    objs.sort(key=lambda x: x.channel_id)

    return objs

def get_karma_dec_summary_objs_list(db, date):
    zone = 'summary'
    query_data = KarmaDec.objects.using(db).filter(date=date)

    objs = []
    obj_dict = {}
    for data in query_data:
        platform, channel_id, user_count, times_count, amount = data.platform, data.channel_id, data.user_count, data.times_count, data.amount
        if channel_id in obj_dict:
            obj = obj_dict[channel_id]
            obj.user_count += user_count
            obj.times_count += times_count
            obj.amount += amount
        else:
            obj = ResourceObject(date, platform, zone, channel_id, user_count, times_count, amount)
            objs.append(obj)
            obj_dict[channel_id] = obj

    objs.sort(key=lambda x: x.channel_id)

    for obj in objs:
        obj.get_str()

    return objs

# 卡牌进化
class CardObject(object):
    def __init__(self, date, zone, user_count, times_count):
        self.date = date
        self.zone = zone
        self.user_count = user_count
        self.times_count = times_count

    def get_str(self):
        self.date_str = _get_date_str(self.date)
        self.zone_str = settings.TABULATE_ZONE_NAME[self.zone]
        self.user_count_str = _get_str_by_int(self.user_count)
        self.times_count_str = _get_str_by_int(self.times_count)

def get_unit_evo_objs_list(db, date, zone):
    query_data = UnitEvo.objects.using(db).filter(date=date, zone=zone)

    objs = []
    for data in query_data:
        user_count, times_count = data.user_count, data.times_count
        obj = CardObject(date, zone, user_count, times_count)
        obj.get_str()
        objs.append(obj)

    return objs

def get_unit_evo_summary_objs_list(db, date):
    zone = 'summary'
    query_data = UnitEvo.objects.using(db).filter(date=date)

    objs = [CardObject(date, zone, 0, 0), ]
    for data in query_data:
        user_count, times_count = data.user_count, data.times_count
        obj = objs[0]
        obj.user_count += user_count
        obj.times_count += times_count

    for obj in objs:
        obj.get_str()

    return objs

# 卡牌强化
def get_unit_mix_objs_list(db, date, zone):
    query_data = UnitMix.objects.using(db).filter(date=date, zone=zone)

    objs = []
    for data in query_data:
        user_count, times_count = data.user_count, data.times_count
        obj = CardObject(date, zone, user_count, times_count)
        obj.get_str()
        objs.append(obj)

    return objs

def get_unit_mix_summary_objs_list(db, date):
    zone = 'summary'
    query_data = UnitMix.objects.using(db).filter(date=date)

    objs = [CardObject(date, zone, 0, 0), ]
    for data in query_data:
        user_count, times_count = data.user_count, data.times_count
        obj = objs[0]
        obj.user_count += user_count
        obj.times_count += times_count

    for obj in objs:
        obj.get_str()

    return objs

# 卡牌出售
def get_unit_sell_objs_list(db, date, zone):
    query_data = UnitSell.objects.using(db).filter(date=date, zone=zone)

    objs = []
    for data in query_data:
        user_count, times_count = data.user_count, data.times_count
        obj = CardObject(date, zone, user_count, times_count)
        obj.get_str()
        objs.append(obj)

    return objs

def get_unit_sell_summary_objs_list(db, date):
    zone = 'summary'
    query_data = UnitSell.objects.using(db).filter(date=date)

    objs = [CardObject(date, zone, 0, 0), ]
    for data in query_data:
        user_count, times_count = data.user_count, data.times_count
        obj = objs[0]
        obj.user_count += user_count
        obj.times_count += times_count

    for obj in objs:
        obj.get_str()

    return objs

# 建筑升级
class FacilityLvupObject(object):
    def __init__(self, date, zone, facility_id, user_count, times_count):
        self.date = date
        self.zone = zone
        self.facility_id = facility_id
        self.user_count = user_count
        self.times_count = times_count

    def get_str(self):
        self.date_str = _get_date_str(self.date)
        self.zone_str = settings.TABULATE_ZONE_NAME[self.zone]
        self.facility_id_str = settings.TABULATE_FACILITY_ID_NAME[self.facility_id]
        self.user_count_str = _get_str_by_int(self.user_count)
        self.times_count_str = _get_str_by_int(self.times_count)

def get_facility_lvup_objs_list(db, date, zone):
    query_data = FacilityLvup.objects.using(db).filter(date=date, zone=zone)

    objs = []
    for data in query_data:
        facility_id, user_count, times_count = data.facility_id, data.user_count, data.times_count
        obj = FacilityLvupObject(date, zone, facility_id, user_count, times_count)
        obj.get_str()
        objs.append(obj)

    objs.sort(key=lambda x: x.facility_id)

    return objs

def get_facility_lvup_summary_objs_list(db, date):
    zone = 'summary'
    query_data = FacilityLvup.objects.using(db).filter(date=date)

    objs = []
    obj_dict = {}
    for data in query_data:
        facility_id, user_count, times_count = data.facility_id, data.user_count, data.times_count
        if facility_id in obj_dict:
            obj = obj_dict[facility_id]
            obj.user_count += user_count
            obj.times_count += times_count
        else:
            obj = FacilityLvupObject(date, zone, facility_id, user_count, times_count)
            objs.append(obj)
            obj_dict[facility_id] = obj

    objs.sort(key=lambda x: x.facility_id)

    for obj in objs:
        obj.get_str()

    return objs

# 资源升级
class LocationLvupObject(object):
    def __init__(self, date, zone, location_id, user_count, times_count):
        self.date = date
        self.zone = zone
        self.location_id = location_id
        self.user_count = user_count
        self.times_count = times_count

    def get_str(self):
        self.date_str = _get_date_str(self.date)
        self.zone_str = settings.TABULATE_ZONE_NAME[self.zone]
        self.location_id_str = settings.TABULATE_LOCATION_ID_NAME[self.location_id]
        self.user_count_str = _get_str_by_int(self.user_count)
        self.times_count_str = _get_str_by_int(self.times_count)

def get_location_lvup_objs_list(db, date, zone):
    query_data = LocationLvup.objects.using(db).filter(date=date, zone=zone)

    objs = []
    for data in query_data:
        location_id, user_count, times_count = data.location_id, data.user_count, data.times_count
        obj = LocationLvupObject(date, zone, location_id, user_count, times_count)
        obj.get_str()
        objs.append(obj)

    objs.sort(key=lambda x: x.location_id)

    return objs

def get_location_lvup_summary_objs_list(db, date):
    zone = 'summary'
    query_data = LocationLvup.objects.using(db).filter(date=date)

    objs = []
    obj_dict = {}
    for data in query_data:
        location_id, user_count, times_count = data.location_id, data.user_count, data.times_count
        if location_id in obj_dict:
            obj = obj_dict[location_id]
            obj.user_count += user_count
            obj.times_count += times_count
        else:
            obj = LocationLvupObject(date, zone, location_id, user_count, times_count)
            objs.append(obj)
            obj_dict[location_id] = obj

    objs.sort(key=lambda x: x.location_id)

    for obj in objs:
        obj.get_str()

    return objs

# 竞技场挑战
class ArenaChallengeObject(object):
    def __init__(self, date, zone, result, user_count, times_count, point_count, karma_count):
        self.date = date
        self.zone = zone
        self.result = result
        self.user_count = user_count
        self.times_count = times_count
        self.point_count = point_count
        self.karma_count = karma_count

    def get_str(self):
        self.date_str = _get_date_str(self.date)
        self.zone_str = settings.TABULATE_ZONE_NAME[self.zone]
        self.result_str = settings.TABULATE_ARENA_CHALLENGE_RESULT_NAME[self.result]
        self.user_count_str = _get_str_by_int(self.user_count)
        self.times_count_str = _get_str_by_int(self.times_count)
        self.point_count_str = _get_str_by_int(self.point_count)
        self.karma_count_str = _get_str_by_int(self.karma_count)

def get_arena_challenge_objs_list(db, date, zone):
    query_data = ArenaChallenge.objects.using(db).filter(date=date, zone=zone)

    objs = []
    for data in query_data:
        result, user_count, times_count, point_count, karma_count = data.result, data.user_count, data.times_count, data.point_count, data.karma_count
        obj = ArenaChallengeObject(date, zone, result, user_count, times_count, point_count, karma_count)
        obj.get_str()
        objs.append(obj)

    objs.sort(key=lambda x: x.result)

    return objs

def get_arena_challenge_summary_objs_list(db, date):
    zone = 'summary'
    query_data = ArenaChallenge.objects.using(db).filter(date=date)

    objs = []
    obj_dict = {}
    for data in query_data:
        result, user_count, times_count, point_count, karma_count = data.result, data.user_count, data.times_count, data.point_count, data.karma_count
        if result in obj_dict:
            obj = obj_dict[result]
            obj.user_count += user_count
            obj.times_count += times_count
            obj.point_count += point_count
            obj.karma_count += karma_count
        else:
            obj = ArenaChallengeObject(date, zone, result, user_count, times_count, point_count, karma_count)
            objs.append(obj)
            obj_dict[result] = obj

    objs.sort(key=lambda x: x.result)

    for obj in objs:
        obj.get_str()

    return objs

# 帝都兰德尔-银钥匙
class DungeonKeyObject(object):
    def __init__(self, date, zone, do_type, user_count, times_count, key_count):
        self.date = date
        self.zone = zone
        self.do_type = do_type
        self.user_count = user_count
        self.times_count = times_count
        self.key_count = key_count

    def get_str(self):
        self.date_str = _get_date_str(self.date)
        self.zone_str = settings.TABULATE_ZONE_NAME[self.zone]
        self.do_type_str = settings.TABULATE_DUNGEON_KEY_DO_TYPE_NAME[self.do_type]
        self.user_count_str = _get_str_by_int(self.user_count)
        self.times_count_str = _get_str_by_int(self.times_count)
        self.key_count_str = _get_str_by_int(self.key_count)

def get_dungeon_sliver_key_objs_list(db, date, zone):
    query_data = DungeonKey.objects.using(db).filter(date=date, zone=zone, key_id=settings.TABULATE_DUNGEON_SLIVER_KEY_CODE)

    objs = []
    for data in query_data:
        do_type, user_count, times_count, key_count = data.do_type, data.user_count, data.times_count, data.key_count
        obj = DungeonKeyObject(date, zone, do_type, user_count, times_count, key_count)
        obj.get_str()
        objs.append(obj)

    objs.sort(key=lambda x: x.do_type)

    return objs

def get_dungeon_sliver_key_summary_objs_list(db, date):
    zone = 'summary'
    query_data = DungeonKey.objects.using(db).filter(date=date, key_id=settings.TABULATE_DUNGEON_SLIVER_KEY_CODE)

    objs = []
    obj_dict = {}
    for data in query_data:
        do_type, user_count, times_count, key_count = data.do_type, data.user_count, data.times_count, data.key_count
        if do_type in obj_dict:
            obj = obj_dict[do_type]
            obj.user_count += user_count
            obj.times_count += times_count
            obj.key_count += key_count
        else:
            obj = DungeonKeyObject(date, zone, do_type, user_count, times_count, key_count)
            objs.append(obj)
            obj_dict[do_type] = obj

    objs.sort(key=lambda x: x.do_type)

    for obj in objs:
        obj.get_str()

    return objs

# 帝都兰德尔-金钥匙
def get_dungeon_gold_key_objs_list(db, date, zone):
    query_data = DungeonKey.objects.using(db).filter(date=date, zone=zone, key_id=settings.TABULATE_DUNGEON_GOLD_KEY_CODE)

    objs = []
    for data in query_data:
        do_type, user_count, times_count, key_count = data.do_type, data.user_count, data.times_count, data.key_count
        obj = DungeonKeyObject(date, zone, do_type, user_count, times_count, key_count)
        obj.get_str()
        objs.append(obj)

    objs.sort(key=lambda x: x.do_type)

    return objs

def get_dungeon_gold_key_summary_objs_list(db, date):
    zone = 'summary'
    query_data = DungeonKey.objects.using(db).filter(date=date, key_id=settings.TABULATE_DUNGEON_GOLD_KEY_CODE)

    objs = []
    obj_dict = {}
    for data in query_data:
        do_type, user_count, times_count, key_count = data.do_type, data.user_count, data.times_count, data.key_count
        if do_type in obj_dict:
            obj = obj_dict[do_type]
            obj.user_count += user_count
            obj.times_count += times_count
            obj.key_count += key_count
        else:
            obj = DungeonKeyObject(date, zone, do_type, user_count, times_count, key_count)
            objs.append(obj)
            obj_dict[do_type] = obj

    objs.sort(key=lambda x: x.do_type)

    for obj in objs:
        obj.get_str()

    return objs

# 黑市刷新
class BmRefreshObject(object):
    def __init__(self, date, zone, money_type, amount, user_count, times_count):
        self.date = date
        self.zone = zone
        self.money_type = money_type
        self.amount = amount
        self.user_count = user_count
        self.times_count = times_count

    def get_str(self):
        self.date_str = _get_date_str(self.date)
        self.zone_str = settings.TABULATE_ZONE_NAME[self.zone]
        self.money_type_str = settings.TABULATE_BM_REFRESH_MONEY_TYPE_NAME[self.money_type]
        self.amount_str = _get_str_by_int(self.amount) 
        self.user_count_str = _get_str_by_int(self.user_count)
        self.times_count_str = _get_str_by_int(self.times_count)

def get_bm_refresh_objs_list(db, date, zone):
    query_data = BmRefresh.objects.using(db).filter(date=date, zone=zone)

    objs = []
    for data in query_data:
        money_type, amount, user_count, times_count = data.money_type, data.amount, data.user_count, data.times_count
        obj = BmRefreshObject(date, zone, money_type, amount, user_count, times_count)
        obj.get_str()
        objs.append(obj)

    objs.sort(key=lambda x: x.money_type)

    return objs

def get_bm_refresh_summary_objs_list(db, date):
    zone = 'summary'
    query_data = BmRefresh.objects.using(db).filter(date=date)

    objs = []
    obj_dict = {}
    for data in query_data:
        money_type, amount, user_count, times_count = data.money_type, data.amount, data.user_count, data.times_count
        if money_type in obj_dict:
            obj = obj_dict[money_type]
            obj.amount += amount
            obj.user_count += user_count
            obj.times_count += times_count
        else:
            obj = BmRefreshObject(date, zone, money_type, amount, user_count, times_count)
            objs.append(obj)
            obj_dict[money_type] = obj

    objs.sort(key=lambda x: x.money_type)

    for obj in objs:
        obj.get_str()

    return objs

# 黑市购买
class BmBuyObject(object):
    def __init__(self, date, zone, money_type, amount, user_count, times_count):
        self.date = date
        self.zone = zone
        self.money_type = money_type
        self.amount = amount
        self.user_count = user_count
        self.times_count = times_count

    def get_str(self):
        self.date_str = _get_date_str(self.date)
        self.zone_str = settings.TABULATE_ZONE_NAME[self.zone]
        self.money_type_str = settings.TABULATE_BM_BUY_MONEY_TYPE_NAME[self.money_type]
        self.amount_str = _get_str_by_int(self.amount) 
        self.user_count_str = _get_str_by_int(self.user_count)
        self.times_count_str = _get_str_by_int(self.times_count)

def get_bm_buy_objs_list(db, date, zone):
    query_data = BmBuy.objects.using(db).filter(date=date, zone=zone)

    objs = []
    for data in query_data:
        money_type, amount, user_count, times_count = data.money_type, data.amount, data.user_count, data.times_count
        obj = BmBuyObject(date, zone, money_type, amount, user_count, times_count)
        obj.get_str()
        objs.append(obj)

    objs.sort(key=lambda x: x.money_type)

    return objs

def get_bm_buy_summary_objs_list(db, date):
    zone = 'summary'
    query_data = BmBuy.objects.using(db).filter(date=date)

    objs = []
    obj_dict = {}
    for data in query_data:
        money_type, amount, user_count, times_count = data.money_type, data.amount, data.user_count, data.times_count
        if money_type in obj_dict:
            obj = obj_dict[money_type]
            obj.amount += amount
            obj.user_count += user_count
            obj.times_count += times_count
        else:
            obj = BmBuyObject(date, zone, money_type, amount, user_count, times_count)
            objs.append(obj)
            obj_dict[money_type] = obj

    objs.sort(key=lambda x: x.money_type)

    for obj in objs:
        obj.get_str()

    return objs

# 黑市物品购买情况
bm_goods_item_type_normal = {
    3: '金币',       #zel
    11:'魂',         #karma
    8: '钻石',       #dia
    2: '友情点',     #friend_p
}
bm_goods_item_type_special = {
    7:'item',    #BRV_ITEM_MST
    6:'unit',    #BRV_UNIT_MST
}

def _get_key(elist):
    key = ''
    for e in elist:
        key += str(e) + ':'
    return key[:-1]

class BmGoodsObject(object):
    def __init__(self, date, zone, item_type, item_id, user_count, times_count, amount):
        self.date = date
        self.zone = zone
        self.item_type = item_type
        self.item_id = item_id
        self.user_count = user_count
        self.times_count = times_count
        self.amount = amount
        
        self.goods_key = _get_key([item_type, item_id])
        self.goods_str = None

    def get_str(self):
        self.date_str = _get_date_str(self.date)
        self.zone_str = settings.TABULATE_ZONE_NAME[self.zone]
        self.user_count_str = _get_str_by_int(self.user_count)
        self.times_count_str = _get_str_by_int(self.times_count)
        self.amount_str = _get_str_by_int(self.amount) 

def get_bm_goods_objs_list(db, date, zone):
    query_data = BmGoods.objects.using(db).filter(date=date, zone=zone)

    bm_goods_item_type_special_db = str(zone) + '_brave_cn_common'

    item_cache = {}
    unit_cache = {}

    objs = []
    for data in query_data:
        item_type, item_id, user_count, times_count, amount = data.item_type, data.item_id, data.user_count, data.times_count, data.amount
        goods_key = _get_key([item_type, item_id])
        obj = BmGoodsObject(date, zone, item_type, item_id, user_count, times_count, amount)
        obj.get_str()

        if item_type in bm_goods_item_type_normal:
            obj.goods_str = bm_goods_item_type_normal[item_id]
        elif item_type in bm_goods_item_type_special:
            if item_type == 7:
                if not item_cache:
                    cache_data = BrvItemMst.objects.using(bm_goods_item_type_special_db)
                    for c_data in cache_data:
                        item_cache[c_data.ITEM_ID] = c_data.ITEM_NAME
                obj.goods_str = item_cache[item_id] if item_id in item_cache else goods_key
            elif item_type ==6:
                if not unit_cache:
                    cache_data = BrvUnitMst.objects.using(bm_goods_item_type_special_db)
                    for c_data in cache_data:
                        unit_cache[c_data.UNIT_ID] = c_data.UNIT_NAME
                obj.goods_str = unit_cache[item_id] if item_id in unit_cache else goods_key
            else:
                obj.goods_str = goods_key
        else:
            obj.goods_str = goods_key

        objs.append(obj)

    return objs

def get_bm_goods_summary_objs_list(db, date):
    zone = 'summary'
    query_data = BmGoods.objects.using(db).filter(date=date)

    item_cache_dict = {}
    unit_cache_dict = {}

    objs = []
    obj_dict = {}
    for data in query_data:
        item_type, item_id, user_count, times_count, amount = data.item_type, data.item_id, data.user_count, data.times_count, data.amount
        
        bm_goods_item_type_special_db = str(data.zone) + '_brave_cn_common'
        
        goods_key = _get_key([item_type, item_id])
        if goods_key in obj_dict:
            obj = obj_dict[goods_key]
            obj.user_count += user_count
            obj.times_count += times_count
            obj.amount += amount
        else:
            obj = BmGoodsObject(date, zone, item_type, item_id, user_count, times_count, amount)
            objs.append(obj)
            obj_dict[goods_key] = obj

        if item_type in bm_goods_item_type_normal:
            obj.goods_str = bm_goods_item_type_normal[item_id]
        elif item_type in bm_goods_item_type_special:
            if item_type == 7:
                if data.zone not in item_cache_dict:
                    item_cache_dict[data.zone] = {}
                    item_cache = item_cache_dict[data.zone]
                    cache_data = BrvItemMst.objects.using(bm_goods_item_type_special_db)
                    for c_data in cache_data:
                        item_cache[c_data.ITEM_ID] = c_data.ITEM_NAME
                item_cache = item_cache_dict[data.zone]
                obj.goods_str = item_cache[item_id] if item_id in item_cache else goods_key
            elif item_type ==6:
                if data.zone not in unit_cache_dict:
                    unit_cache_dict[data.zone] = {}
                    unit_cache = unit_cache_dict[data.zone]
                    cache_data = BrvUnitMst.objects.using(bm_goods_item_type_special_db)
                    for c_data in cache_data:
                        unit_cache[c_data.UNIT_ID] = c_data.UNIT_NAME
                unit_cache = unit_cache_dict[data.zone]
                obj.goods_str = unit_cache[item_id] if item_id in unit_cache else goods_key
            else:
                obj.goods_str = goods_key
        else:
            obj.goods_str = goods_key

    for obj in objs:
        obj.get_str()

    return objs












