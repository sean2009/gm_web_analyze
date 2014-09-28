# -*- coding: utf-8 -*-

from django.db import models

################################################################################
# 日报数据 表
################################################################################

# 每日新增设备数
class DeviceCount(models.Model):
    date = models.CharField(max_length=32, primary_key=True)
    cnt = models.IntegerField()

    class Meta:
        db_table = 'device_count'

# 每日平台新增设备数
class PlatformDeviceCount(models.Model):
    date = models.CharField(max_length=32, primary_key=True)
    platform = models.IntegerField(primary_key=True)
    cnt = models.IntegerField()

    class Meta:
        db_table = 'platform_device_count'
        unique_together = ('date', 'platform')

# 每日渠道新增设备数
class ChannelDeviceCount(models.Model):
    date = models.CharField(max_length=32, primary_key=True)
    channel_id = models.CharField(max_length=20, primary_key=True)
    cnt = models.IntegerField()

    class Meta:
        db_table = 'channel_device_count'
        unique_together = ('date', 'channel_id')

# 每日新增用户数
class UserCount(models.Model):
    date = models.CharField(max_length=32, primary_key=True)
    cnt = models.IntegerField()

    class Meta:
        db_table = 'user_count'

# 每日平台新增用户数
class PlatformUserCount(models.Model):
    date = models.CharField(max_length=32, primary_key=True)
    platform = models.IntegerField(primary_key=True)
    cnt = models.IntegerField()

    class Meta:
        db_table = 'platform_user_count'
        unique_together = ('date', 'platform')

# 每日渠道新增用户数
class ChannelUserCount(models.Model):
    date = models.CharField(max_length=32, primary_key=True)
    channel_id = models.CharField(max_length=20, primary_key=True)
    cnt = models.IntegerField()

    class Meta:
        db_table = 'channel_user_count'
        unique_together = ('date', 'channel_id')

# 每日登录用户数
class UserLogin(models.Model):
    date = models.CharField(max_length=32, primary_key=True)
    cnt = models.IntegerField()

    class Meta:
        db_table = 'user_login'

# 每日平台登录用户数
class PlatformUserLogin(models.Model):
    date = models.CharField(max_length=32, primary_key=True)
    platform = models.IntegerField(primary_key=True)
    cnt = models.IntegerField()

    class Meta:
        db_table = 'platform_user_login'
        unique_together = ('date', 'platform')

# 每日渠道登录用户数
class ChannelUserLogin(models.Model):
    date = models.CharField(max_length=32, primary_key=True)
    channel_id = models.CharField(max_length=20, primary_key=True)
    cnt = models.IntegerField()

    class Meta:
        db_table = 'channel_user_login'
        unique_together = ('date', 'channel_id')

# 每日登录设备数
class Dau(models.Model):
    date = models.CharField(max_length=32, primary_key=True)
    cnt = models.IntegerField()

    class Meta:
        db_table = 'dau'

# 每日平台登录设备数
class PlatformDau(models.Model):
    date = models.CharField(max_length=32, primary_key=True)
    platform = models.IntegerField(primary_key=True)
    cnt = models.IntegerField()

    class Meta:
        db_table = 'platform_dau'
        unique_together = ('date', 'platform')

# 每日渠道登录设备数
class ChannelDau(models.Model):
    date = models.CharField(max_length=32, primary_key=True)
    channel_id = models.CharField(max_length=20, primary_key=True)
    cnt = models.IntegerField()

    class Meta:
        db_table = 'channel_dau'
        unique_together = ('date', 'channel_id')

# 次日留存
class Lc1(models.Model):
    date = models.CharField(max_length=32, primary_key=True)
    cnt = models.IntegerField()

    class Meta:
        db_table = 'lc1'

# 平台次日留存
class PlatformLc1(models.Model):
    date = models.CharField(max_length=32, primary_key=True)
    platform = models.IntegerField(primary_key=True)
    cnt = models.IntegerField()

    class Meta:
        db_table = 'platform_lc1'
        unique_together = ('date', 'platform')

# 渠道次日留存
class ChannelLc1(models.Model):
    date = models.CharField(max_length=32, primary_key=True)
    channel_id = models.CharField(max_length=20, primary_key=True)
    cnt = models.IntegerField()

    class Meta:
        db_table = 'channel_lc1'
        unique_together = ('date', 'channel_id')

# 2日留存
class Lc2(models.Model):
    date = models.CharField(max_length=32, primary_key=True)
    cnt = models.IntegerField()

    class Meta:
        db_table = 'lc2'

# 平台2日留存
class PlatformLc2(models.Model):
    date = models.CharField(max_length=32, primary_key=True)
    platform = models.IntegerField(primary_key=True)
    cnt = models.IntegerField()

    class Meta:
        db_table = 'platform_lc2'
        unique_together = ('date', 'platform')

# 渠道2日留存
class ChannelLc2(models.Model):
    date = models.CharField(max_length=32, primary_key=True)
    channel_id = models.CharField(max_length=20, primary_key=True)
    cnt = models.IntegerField()

    class Meta:
        db_table = 'channel_lc2'
        unique_together = ('date', 'channel_id')

# 3日留存
class Lc3(models.Model):
    date = models.CharField(max_length=32, primary_key=True)
    cnt = models.IntegerField()

    class Meta:
        db_table = 'lc3'

# 平台3日留存
class PlatformLc3(models.Model):
    date = models.CharField(max_length=32, primary_key=True)
    platform = models.IntegerField(primary_key=True)
    cnt = models.IntegerField()

    class Meta:
        db_table = 'platform_lc3'
        unique_together = ('date', 'platform')

# 渠道3日留存
class ChannelLc3(models.Model):
    date = models.CharField(max_length=32, primary_key=True)
    channel_id = models.CharField(max_length=20, primary_key=True)
    cnt = models.IntegerField()

    class Meta:
        db_table = 'channel_lc3'
        unique_together = ('date', 'channel_id')

# 4日留存
class Lc4(models.Model):
    date = models.CharField(max_length=32, primary_key=True)
    cnt = models.IntegerField()

    class Meta:
        db_table = 'lc4'

# 平台4日留存
class PlatformLc4(models.Model):
    date = models.CharField(max_length=32, primary_key=True)
    platform = models.IntegerField(primary_key=True)
    cnt = models.IntegerField()

    class Meta:
        db_table = 'platform_lc4'
        unique_together = ('date', 'platform')

# 渠道4日留存
class ChannelLc4(models.Model):
    date = models.CharField(max_length=32, primary_key=True)
    channel_id = models.CharField(max_length=20, primary_key=True)
    cnt = models.IntegerField()

    class Meta:
        db_table = 'channel_lc4'
        unique_together = ('date', 'channel_id')

# 5日留存
class Lc5(models.Model):
    date = models.CharField(max_length=32, primary_key=True)
    cnt = models.IntegerField()

    class Meta:
        db_table = 'lc5'

# 平台5日留存
class PlatformLc5(models.Model):
    date = models.CharField(max_length=32, primary_key=True)
    platform = models.IntegerField(primary_key=True)
    cnt = models.IntegerField()

    class Meta:
        db_table = 'platform_lc5'
        unique_together = ('date', 'platform')

# 渠道5日留存
class ChannelLc5(models.Model):
    date = models.CharField(max_length=32, primary_key=True)
    channel_id = models.CharField(max_length=20, primary_key=True)
    cnt = models.IntegerField()

    class Meta:
        db_table = 'channel_lc5'
        unique_together = ('date', 'channel_id')

# 6日留存
class Lc6(models.Model):
    date = models.CharField(max_length=32, primary_key=True)
    cnt = models.IntegerField()

    class Meta:
        db_table = 'lc6'

# 平台6日留存
class PlatformLc6(models.Model):
    date = models.CharField(max_length=32, primary_key=True)
    platform = models.IntegerField(primary_key=True)
    cnt = models.IntegerField()

    class Meta:
        db_table = 'platform_lc6'
        unique_together = ('date', 'platform')

# 渠道6日留存
class ChannelLc6(models.Model):
    date = models.CharField(max_length=32, primary_key=True)
    channel_id = models.CharField(max_length=20, primary_key=True)
    cnt = models.IntegerField()

    class Meta:
        db_table = 'channel_lc6'
        unique_together = ('date', 'channel_id')

# 7日留存
class Lc7(models.Model):
    date = models.CharField(max_length=32, primary_key=True)
    cnt = models.IntegerField()

    class Meta:
        db_table = 'lc7'

# 平台7日留存
class PlatformLc7(models.Model):
    date = models.CharField(max_length=32, primary_key=True)
    platform = models.IntegerField(primary_key=True)
    cnt = models.IntegerField()

    class Meta:
        db_table = 'platform_lc7'
        unique_together = ('date', 'platform')

# 渠道7日留存
class ChannelLc7(models.Model):
    date = models.CharField(max_length=32, primary_key=True)
    channel_id = models.CharField(max_length=20, primary_key=True)
    cnt = models.IntegerField()

    class Meta:
        db_table = 'channel_lc7'
        unique_together = ('date', 'channel_id')

# 14日留存
class Lc14(models.Model):
    date = models.CharField(max_length=32, primary_key=True)
    cnt = models.IntegerField()

    class Meta:
        db_table = 'lc14'

# 平台14日留存
class PlatformLc14(models.Model):
    date = models.CharField(max_length=32, primary_key=True)
    platform = models.IntegerField(primary_key=True)
    cnt = models.IntegerField()

    class Meta:
        db_table = 'platform_lc14'
        unique_together = ('date', 'platform')

# 渠道14日留存
class ChannelLc14(models.Model):
    date = models.CharField(max_length=32, primary_key=True)
    channel_id = models.CharField(max_length=20, primary_key=True)
    cnt = models.IntegerField()

    class Meta:
        db_table = 'channel_lc14'
        unique_together = ('date', 'channel_id')

# 30日留存
class Lc30(models.Model):
    date = models.CharField(max_length=32, primary_key=True)
    cnt = models.IntegerField()

    class Meta:
        db_table = 'lc30'

# 平台30日留存
class PlatformLc30(models.Model):
    date = models.CharField(max_length=32, primary_key=True)
    platform = models.IntegerField(primary_key=True)
    cnt = models.IntegerField()

    class Meta:
        db_table = 'platform_lc30'
        unique_together = ('date', 'platform')

# 渠道30日留存
class ChannelLc30(models.Model):
    date = models.CharField(max_length=32, primary_key=True)
    channel_id = models.CharField(max_length=20, primary_key=True)
    cnt = models.IntegerField()

    class Meta:
        db_table = 'channel_lc30'
        unique_together = ('date', 'channel_id')

# 每日付费角色数
class VipCount(models.Model):
    date = models.CharField(max_length=32, primary_key=True)
    cnt = models.IntegerField()

    class Meta:
        db_table = 'vip_count'

# 每日平台付费角色数
class PlatformVipCount(models.Model):
    date = models.CharField(max_length=32, primary_key=True)
    platform = models.IntegerField(primary_key=True)
    cnt = models.IntegerField()

    class Meta:
        db_table = 'platform_vip_count'
        unique_together = ('date', 'platform')

# 每日渠道付费角色数
class ChannelVipCount(models.Model):
    date = models.CharField(max_length=32, primary_key=True)
    channel_id = models.CharField(max_length=20, primary_key=True)
    cnt = models.IntegerField()

    class Meta:
        db_table = 'channel_vip_count'
        unique_together = ('date', 'channel_id')

# 每日付费金额
class VipAmount(models.Model):
    date = models.CharField(max_length=32, primary_key=True)
    cnt = models.IntegerField()

    class Meta:
        db_table = 'vip_amount'

# 每日平台付费金额
class PlatformVipAmount(models.Model):
    date = models.CharField(max_length=32, primary_key=True)
    platform = models.IntegerField(primary_key=True)
    cnt = models.IntegerField()

    class Meta:
        db_table = 'platform_vip_amount'
        unique_together = ('date', 'platform')

# 每日渠道付费金额
class ChannelVipAmount(models.Model):
    date = models.CharField(max_length=32, primary_key=True)
    channel_id = models.CharField(max_length=20, primary_key=True)
    cnt = models.IntegerField()

    class Meta:
        db_table = 'channel_vip_amount'
        unique_together = ('date', 'channel_id')

# 每日订单成功失败数
class Purchase(models.Model):
    date = models.CharField(max_length=32, primary_key=True)
    suc = models.IntegerField()
    fail = models.IntegerField()

    class Meta:
        db_table = 'purchase'

# 每日平台订单成功失败数
class PlatformPurchase(models.Model):
    date = models.CharField(max_length=32, primary_key=True)
    platform = models.IntegerField(primary_key=True)
    suc = models.IntegerField()
    fail = models.IntegerField()

    class Meta:
        db_table = 'platform_purchase'
        unique_together = ('date', 'platform')

# 每日渠道订单成功失败数
class ChannelPurchase(models.Model):
    date = models.CharField(max_length=32, primary_key=True)
    channel_id = models.CharField(max_length=20, primary_key=True)
    suc = models.IntegerField()
    fail = models.IntegerField()

    class Meta:
        db_table = 'channel_purchase'
        unique_together = ('date', 'channel_id')

################################################################################
# 行为数据 表
################################################################################

# 充值档次
class PaymentLevel(models.Model):
    date = models.CharField(max_length=32, primary_key=True)
    platform = models.IntegerField()
    zone = models.CharField(max_length=32, primary_key=True)
    purchase_id = models.IntegerField(primary_key=True)
    user_count = models.IntegerField()
    times_count = models.IntegerField()
    amount = models.IntegerField()

    class Meta:
        db_table = 'payment_level'
        unique_together = ('date', 'zone', 'purchase_id')

# 金币产出
class ZelInc(models.Model):
    date = models.CharField(max_length=32, primary_key=True)
    platform = models.IntegerField()
    zone = models.CharField(max_length=32, primary_key=True)
    channel_id = models.IntegerField(primary_key=True)
    user_count = models.IntegerField()
    times_count = models.IntegerField()
    amount = models.IntegerField()

    class Meta:
        db_table = 'zel_inc'
        unique_together = ('date', 'zone', 'channel_id')

# 金币消耗
class ZelDec(models.Model):
    date = models.CharField(max_length=32, primary_key=True)
    platform = models.IntegerField()
    zone = models.CharField(max_length=32, primary_key=True)
    channel_id = models.IntegerField(primary_key=True)
    user_count = models.IntegerField()
    times_count = models.IntegerField()
    amount = models.IntegerField()

    class Meta:
        db_table = 'zel_dec'
        unique_together = ('date', 'zone', 'channel_id')

# 钻石产出
class DiaInc(models.Model):
    date = models.CharField(max_length=32, primary_key=True)
    platform = models.IntegerField()
    zone = models.CharField(max_length=32, primary_key=True)
    channel_id = models.IntegerField(primary_key=True)
    user_count = models.IntegerField()
    times_count = models.IntegerField()
    amount = models.IntegerField()

    class Meta:
        db_table = 'dia_inc'
        unique_together = ('date', 'zone', 'channel_id')

# 钻石消耗
class DiaDec(models.Model):
    date = models.CharField(max_length=32, primary_key=True)
    platform = models.IntegerField()
    zone = models.CharField(max_length=32, primary_key=True)
    channel_id = models.IntegerField(primary_key=True)
    user_count = models.IntegerField()
    times_count = models.IntegerField()
    amount = models.IntegerField()

    class Meta:
        db_table = 'dia_dec'
        unique_together = ('date', 'zone', 'channel_id')

# 魂产出
class KarmaInc(models.Model):
    date = models.CharField(max_length=32, primary_key=True)
    platform = models.IntegerField()
    zone = models.CharField(max_length=32, primary_key=True)
    channel_id = models.IntegerField(primary_key=True)
    user_count = models.IntegerField()
    times_count = models.IntegerField()
    amount = models.IntegerField()

    class Meta:
        db_table = 'karma_inc'
        unique_together = ('date', 'zone', 'channel_id')

# 魂消耗
class KarmaDec(models.Model):
    date = models.CharField(max_length=32, primary_key=True)
    platform = models.IntegerField()
    zone = models.CharField(max_length=32, primary_key=True)
    channel_id = models.IntegerField(primary_key=True)
    user_count = models.IntegerField()
    times_count = models.IntegerField()
    amount = models.IntegerField()

    class Meta:
        db_table = 'karma_dec'
        unique_together = ('date', 'zone', 'channel_id')

# 当日创角等级分布
class NewUserLevel(models.Model):
    date = models.CharField(max_length=32, primary_key=True)
    zone = models.CharField(max_length=32, primary_key=True)
    lv = models.IntegerField(primary_key=True)
    count = models.IntegerField()

    class Meta:
        db_table = 'new_user_level'
        unique_together = ('date', 'zone', 'lv')

# 竞技场挑战
class ArenaChallenge(models.Model):
    date = models.CharField(max_length=32, primary_key=True)
    zone = models.CharField(max_length=32, primary_key=True)
    result = models.IntegerField(primary_key=True)
    user_count = models.IntegerField()
    times_count = models.IntegerField()
    point_count = models.IntegerField()
    karma_count = models.IntegerField()

    class Meta:
        db_table = 'arena_challenge'
        unique_together = ('date', 'zone', 'result')

# 钥匙
class DungeonKey(models.Model):
    date = models.CharField(max_length=32, primary_key=True)
    zone = models.CharField(max_length=32, primary_key=True)
    do_type = models.IntegerField(primary_key=True)
    key_id = models.IntegerField(primary_key=True)
    user_count = models.IntegerField()
    times_count = models.IntegerField()
    key_count = models.IntegerField()

    class Meta:
        db_table = 'dungeon_key'
        unique_together = ('date', 'zone', 'do_type', 'key_id')

# 进化
class UnitEvo(models.Model):
    date = models.CharField(max_length=32, primary_key=True)
    zone = models.CharField(max_length=32, primary_key=True)
    user_count = models.IntegerField()
    times_count = models.IntegerField()

    class Meta:
        db_table = 'unit_evo'
        unique_together = ('date', 'zone')

# 强化
class UnitMix(models.Model):
    date = models.CharField(max_length=32, primary_key=True)
    zone = models.CharField(max_length=32, primary_key=True)
    user_count = models.IntegerField()
    times_count = models.IntegerField()

    class Meta:
        db_table = 'unit_mix'
        unique_together = ('date', 'zone')

# 出售
class UnitSell(models.Model):
    date = models.CharField(max_length=32, primary_key=True)
    zone = models.CharField(max_length=32, primary_key=True)
    user_count = models.IntegerField()
    times_count = models.IntegerField()

    class Meta:
        db_table = 'unit_sell'
        unique_together = ('date', 'zone')

# 建筑升级 
class FacilityLvup(models.Model):
    date = models.CharField(max_length=32, primary_key=True)
    zone = models.CharField(max_length=32, primary_key=True)
    facility_id = models.IntegerField(primary_key=True)
    user_count = models.IntegerField()
    times_count = models.IntegerField()

    class Meta:
        db_table = 'facility_lvup'
        unique_together = ('date', 'zone', 'facility_id')

# 资源升级 
class LocationLvup(models.Model):
    date = models.CharField(max_length=32, primary_key=True)
    zone = models.CharField(max_length=32, primary_key=True)
    location_id = models.IntegerField(primary_key=True)
    user_count = models.IntegerField()
    times_count = models.IntegerField()

    class Meta:
        db_table = 'location_lvup'
        unique_together = ('date', 'zone', 'location_id')

# 黑市刷新
class BmRefresh(models.Model):
    date = models.CharField(max_length=32, primary_key=True)
    zone = models.CharField(max_length=32, primary_key=True)
    money_type = models.IntegerField(primary_key=True)
    amount = models.IntegerField()
    user_count = models.IntegerField()
    times_count = models.IntegerField()

    class Meta:
        db_table = 'bm_refresh'
        unique_together = ('date', 'zone', 'money_type')

# 黑市购买
class BmBuy(models.Model):
    date = models.CharField(max_length=32, primary_key=True)
    zone = models.CharField(max_length=32, primary_key=True)
    money_type = models.IntegerField(primary_key=True)
    amount = models.IntegerField()
    user_count = models.IntegerField()
    times_count = models.IntegerField()

    class Meta:
        db_table = 'bm_buy'
        unique_together = ('date', 'zone', 'money_type')

# 黑市物品购买
class BmGoods(models.Model):
    date = models.CharField(max_length=32, primary_key=True)
    zone = models.CharField(max_length=32, primary_key=True)
    item_type = models.IntegerField(primary_key=True)
    item_id = models.IntegerField(primary_key=True)
    user_count = models.IntegerField()
    times_count = models.IntegerField()
    amount = models.IntegerField()

    class Meta:
        db_table = 'bm_goods'
        unique_together = ('date', 'zone', 'item_type', 'item_id')

################################################################################
# 监控数据 表
################################################################################

# 当日充值榜
class TopVip(models.Model):
    date = models.CharField(max_length=32, primary_key=True)
    platform = models.IntegerField()
    zone = models.CharField(max_length=32, primary_key=True)
    user_id = models.CharField(max_length=32, primary_key=True)
    channel_id = models.IntegerField()
    amount = models.IntegerField()
    times = models.IntegerField()

    class Meta:
        db_table = 'top_vip'
        unique_together = ('date', 'zone', 'user_id')

# 钻石榜
class TopDia(models.Model):
    date = models.CharField(max_length=32, primary_key=True)
    platform = models.IntegerField()
    zone = models.CharField(max_length=32, primary_key=True)
    user_id = models.CharField(max_length=32, primary_key=True)
    channel_id = models.IntegerField()
    amount = models.IntegerField()
    times = models.IntegerField()
    do_type = models.IntegerField(primary_key=True)

    class Meta:
        db_table = 'top_dia'
        unique_together = ('date', 'zone', 'user_id', 'do_type')

# 金币榜
class TopZel(models.Model):
    date = models.CharField(max_length=32, primary_key=True)
    platform = models.IntegerField()
    zone = models.CharField(max_length=32, primary_key=True)
    user_id = models.CharField(max_length=32, primary_key=True)
    channel_id = models.IntegerField()
    amount = models.IntegerField()
    times = models.IntegerField()
    do_type = models.IntegerField(primary_key=True)

    class Meta:
        db_table = 'top_zel'
        unique_together = ('date', 'zone', 'user_id', 'do_type')

# 魂榜
class TopKarma(models.Model):
    date = models.CharField(max_length=32, primary_key=True)
    platform = models.IntegerField()
    zone = models.CharField(max_length=32, primary_key=True)
    user_id = models.CharField(max_length=32, primary_key=True)
    channel_id = models.IntegerField()
    amount = models.IntegerField()
    times = models.IntegerField()
    do_type = models.IntegerField(primary_key=True)

    class Meta:
        db_table = 'top_karma'
        unique_together = ('date', 'zone', 'user_id', 'do_type')

# 充值预警榜
class Vip7(models.Model):
    zone = models.CharField(max_length=32)
    user_id = models.CharField(max_length=32)
    channel_id = models.CharField(max_length=20)
    platform = models.IntegerField()
    amount3 = models.IntegerField()
    amount7 = models.IntegerField(primary_key=True)

    class Meta:
        db_table = 'vip7'

################################################################################
# 额外 表
################################################################################
class BrvItemMst(models.Model):
    ITEM_ID = models.IntegerField(primary_key=True)
    ITEM_NAME = models.CharField(max_length=32)
    ITEM_NAME_S = models.CharField(max_length=32)
    ITEM_TYPE = models.IntegerField()
    ITEM_KBN = models.IntegerField()
    ITEM_IMG = models.CharField(max_length=32)
    ICON_TYPE = models.IntegerField()
    RARE = models.IntegerField()
    DISPORDER = models.IntegerField() 
    COLOR = models.IntegerField()
    AMOUNT_SELL = models.IntegerField()
    EFFECT_GROUP_ID = models.IntegerField()
    TARGET = models.IntegerField()
    EFFECT_RANGE = models.IntegerField()
    PROCESS_TYPE = models.CharField(max_length=255)
    PROCESS_PARAM = models.CharField(max_length=255)
    FRAME_MAX_POSSESSION = models.IntegerField()
    EQP_MAX_POSSESSION = models.IntegerField()
    DISP_DICTIONARY = models.IntegerField()
    DESCRIPTION = models.CharField(max_length=255)
    MESSAGE = models.CharField(max_length=255)
    SOURCE = models.CharField(max_length=255)
    RAID_FLG = models.IntegerField()
    RAID_USAGE_TYPE = models.IntegerField()
    STATE = models.IntegerField()
    CREATEDATE = models.DateTimeField()
    UPDATEDATE = models.DateTimeField()
    ITEM_KIND = models.IntegerField()
    
    class Meta:
        db_table = 'BRV_ITEM_MST'

class BrvUnitMst(models.Model):
    UNIT_ID = models.IntegerField(primary_key=True)
    UNIT_NAME = models.CharField(max_length=32)
    RARE = models.IntegerField()
    COST = models.IntegerField()
    TRIBE = models.IntegerField()
    SEX = models.IntegerField()
    SERIES = models.IntegerField()
    MAX_LV = models.IntegerField()
    PATTERN_ID = models.CharField(max_length=32)
    GROWTH_TYPE = models.IntegerField()
    MIN_HP = models.IntegerField()
    MAX_HP = models.IntegerField()
    MIN_ATK = models.IntegerField()
    MAX_ATK = models.IntegerField()
    MIN_DEF = models.IntegerField()
    MAX_DEF = models.IntegerField()
    MIN_HEL = models.IntegerField()
    MAX_HEL = models.IntegerField()
    STATUS_RESIST = models.CharField(max_length=32)
    ELEMENT = models.IntegerField()
    EFFECT_FRAME = models.CharField(max_length=255)
    DAMAGE_FRAME = models.CharField(max_length=255)
    DROP_REPEAT_CNT = models.IntegerField()
    MOVE_SPEED = models.IntegerField()
    MOVE_TYPE1 = models.IntegerField()
    MOVE_TYPE2 = models.IntegerField()
    MOVE_TYPE_SKILL = models.IntegerField()
    MOVE_OFFSET = models.CharField(max_length=32)
    AFTERIMAGE = models.IntegerField()
    AI_TYPE = models.IntegerField()
    LEADER_SKILL_ID = models.IntegerField()
    SKILL_ID = models.IntegerField()
    EXTRA_SKILL_ID = models.IntegerField()
    DISPORDER = models.IntegerField()
    SOUND_SETTING = models.CharField(max_length=255)
    IMG_CGG = models.CharField(max_length=32)
    HOME_IMG_POS = models.CharField(max_length=32)
    DETAIL_IMG_POS = models.CharField(max_length=32)
    CONFIRM_IMG_POS = models.CharField(max_length=32)
    SUMMON_IMG_POS = models.CharField(max_length=32)
    CUT_IN_IMG_POS = models.CharField(max_length=32)
    HP_DISP_POS = models.CharField(max_length=32)
    ADJUST_EXP = models.IntegerField()
    ADJUST_SKILL_LVUP_RATE = models.IntegerField()
    AMOUNT_SELL = models.IntegerField()
    DESCRIPTION = models.CharField(max_length=255)
    SOURCE = models.CharField(max_length=255)
    STATE = models.IntegerField()
    CREATEDATE = models.DateTimeField()
    UPDATEDATE = models.DateTimeField()
    KIND = models.IntegerField()
    PARAM_MAX = models.CharField(max_length=32)
    
    class Meta:
        db_table = 'BRV_UNIT_MST'

class BrvUserInfo(models.Model):
    USER_ID = models.CharField(max_length=32, primary_key=True)
    HANDLE_NAME = models.CharField(max_length=32)
    ACCOUNT_ID = models.CharField(max_length=32)
    PASSWORD = models.CharField(max_length=32)
    MODEL_CHANGE_CNT = models.IntegerField()
    FRIEND_ID = models.CharField(max_length=32)
    CONTACT_ID = models.CharField(max_length=32)
    OS = models.IntegerField()
    PLATFORM = models.IntegerField()
    CHANNEL = models.CharField(max_length=10)
    CHANNEL_USER_ID = models.CharField(max_length=64)
    CHANNEL_TOKEN = models.CharField(max_length=64)
    MODEL = models.CharField(max_length=255)
    DEVICE_ID = models.CharField(max_length=255)
    DEVICE_TOKEN = models.CharField(max_length=255)
    APP_VERSION = models.IntegerField()
    TUTORIAL_INFO = models.CharField(max_length=255)
    TUTORIAL_PRESENT_SEND_FLAG = models.IntegerField()
    TUTORIAL_END = models.IntegerField()
    TUTORIAL_END_DATE = models.IntegerField()
    TUTORIAL_MARK = models.IntegerField()
    STARTDATE = models.IntegerField()
    START_ELEMENT = models.IntegerField()
    SCENARIO_INFO = models.TextField()
    EVENT_SCENARIO_INFO = models.TextField()
    HANDLE_NAME_OLD = models.CharField(max_length=32)
    HANDLE_NAME_CHGDATE = models.DateTimeField()
    STATE = models.IntegerField()
    CREATEDATE = models.DateTimeField()
    UPDATEDATE = models.DateTimeField()

    class Meta:
        db_table = 'BRV_USER_INFO'

class BrvUserTeamInfo(models.Model):
    USER_ID = models.CharField(max_length=32, primary_key=True)
    LV = models.IntegerField()
    EXP = models.IntegerField()
    ACTION_P = models.IntegerField()
    MAX_ACTION_P = models.IntegerField()
    ACTION_TIMER = models.IntegerField()
    FIGHT_P = models.IntegerField()
    MAX_FIGHT_P = models.IntegerField()
    FIGHT_TIMER = models.IntegerField()
    MAX_UNIT_CNT = models.IntegerField()
    ADD_UNIT_CNT = models.IntegerField()
    DECK_COST = models.IntegerField()
    CURRENT_DECK_NO = models.IntegerField()
    MAX_FRD_CNT = models.IntegerField()
    MAX_WAREHOUSE_CNT = models.IntegerField()
    ADD_WAREHOUSE_CNT = models.IntegerField()
    FRIEND_P = models.IntegerField()
    ZEL = models.IntegerField()
    KARMA = models.IntegerField()
    BRAVE_COIN = models.IntegerField()
    FRIEND_MESSAGE = models.CharField(max_length=255)
    WANT_GIFT = models.CharField(max_length=255)
    LOGIN_DATE = models.IntegerField()
    SERIAL_LOGIN_DAY = models.IntegerField()
    STATE = models.IntegerField()
    VIP_EXPIRY_DATE = models.DateTimeField()
    VIP_CLIAM_GIFT_DATE = models.DateTimeField()
    BUY_GIFTPACK_DATE = models.DateTimeField()
    CREATEDATE = models.DateTimeField()
    UPDATEDATE = models.DateTimeField()

    class Meta:
        db_table = 'BRV_USER_TEAM_INFO'
