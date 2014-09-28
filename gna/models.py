# -*- coding: utf-8 -*-

from django.db import models

class DailyCache(models.Model):
    """
    每日数据存放
    """
    key   = models.CharField(max_length=255, null=False, db_index=True)
    date  = models.DateField(null=False)
    value = models.CharField(max_length=255, null=False)

    class Meta:
        db_table = 'gna_daily_cache'
        unique_together = ('key', 'date')


class SimpleCache(models.Model):
    """
    普通
    """
    key   = models.CharField(max_length=255, null=False, primary_key=True)
    value = models.CharField(max_length=255, null=True)

    class Meta:
        db_table = 'gna_simple_cache'


class DeltaCache(models.Model):
    """
    时间步进
    """
    key      = models.CharField(max_length=255, null=False, primary_key=True)
    datetime = models.DateTimeField(null=False)
    value    = models.CharField(max_length=255, null=False)

    class Meta:
        db_table = 'gna_delta_cache'


class DailyFlagCache(models.Model):
    """
    标记每日数据是否为完整数据（一整天的数据）
    """
    key   = models.CharField(max_length=255, null=False, db_index=True)
    date  = models.DateField(null=False)
    value = models.BooleanField(default=False)

    class Meta:
        db_table = 'gna_daily_flag_cache'
        unique_together = ('key', 'date')

# # 今日登录用户临时表
# class TodayAccessTmp(models.Model):
#     osuser_id = models.CharField(max_length=255, primary_key=True)

# # 前x天注册用户临时表
# class RegisterUser1Tmp(models.Model):
#     osuser_id = models.CharField(max_length=255, primary_key=True)

# class RegisterUser2Tmp(models.Model):
#     osuser_id = models.CharField(max_length=255, primary_key=True)

# class RegisterUser3Tmp(models.Model):
#     osuser_id = models.CharField(max_length=255, primary_key=True)

# class RegisterUser4Tmp(models.Model):
#     osuser_id = models.CharField(max_length=255, primary_key=True)

# class RegisterUser5Tmp(models.Model):
#     osuser_id = models.CharField(max_length=255, primary_key=True)

# class RegisterUser6Tmp(models.Model):
#     osuser_id = models.CharField(max_length=255, primary_key=True)

# class RegisterUser7Tmp(models.Model):
#     osuser_id = models.CharField(max_length=255, primary_key=True)

# class RegisterUser14Tmp(models.Model):
#     osuser_id = models.CharField(max_length=255, primary_key=True)

# class RegisterUser30Tmp(models.Model):
#     osuser_id = models.CharField(max_length=255, primary_key=True)

# class RegisterUser60Tmp(models.Model):
#     osuser_id = models.CharField(max_length=255, primary_key=True)

# class RegisterUser90Tmp(models.Model):
#     osuser_id = models.CharField(max_length=255, primary_key=True)



















