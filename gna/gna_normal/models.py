# -*- coding: utf-8 -*-

from django.db import models

class Player(models.Model):
    osuser_id  = models.CharField(max_length=255, primary_key=True)
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)
    is_closed  = models.BooleanField(default=False)
    closed_at  = models.DateTimeField(default=None)

    class Meta:
        db_table = 'player_player'


class DailyAccessLog(models.Model):
    """
    每日访问记录
    """
    osuser_id     = models.CharField(u'玩家id', max_length=50)
    accessed_at   = models.DateTimeField(u'访问时间',auto_now_add=True, db_index=True)
    is_smartphone = models.BooleanField(u'智能手机', default=False)
    device        = models.IntegerField(u'设备类型', default=0)

    class Meta:
        db_table = 'gamelog_dailyaccesslog'
        verbose_name = verbose_name_plural = u"每日访问记录"


class PaymentInfo(models.Model):
    """
    购买信息
    """
    osuser_id  = models.CharField(u'玩家id', max_length=50, null=False, db_index=True)
    item_id    = models.IntegerField(u'产品id', max_length=50, null=False)
    point      = models.IntegerField(u'结算费用', null=False)
    quantity   = models.IntegerField('购买数量', default=1)
    send_data  = models.TextField(u'原始发送的数据', null=False)
    point_code = models.CharField(u'结算代码', max_length=50, unique=True)
    point_date = models.CharField(u'结算信息创建时间(UTC)', max_length=50, blank=True)
    point_url  = models.URLField(u'移动端接口URL', max_length=255, blank=True)
    recv_data  = models.TextField(u'原始收到的数据', null=True)
    status     = models.CharField(u'购买状态', max_length=50, null=True, blank=True)
    device     = models.IntegerField(u'设备类型', default=1)
    created_at = models.DateTimeField(u'创建时间', auto_now_add=True, editable=False, db_index=True)

    class Meta:
        db_table = 'gsocial_paymentinfo'
        verbose_name = verbose_name_plural = u"购买记录"


