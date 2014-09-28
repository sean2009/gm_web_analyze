# -*- coding: utf-8 -*-

from django.conf import settings
from django.db import transaction
import datetime

from gna.common import (
    date_to_datetime_begin,
    date_to_datetime_end,
    div_operation,
    get_retention_cache_key,
    parse_retention_cache_key,
    topo_sort,
)
from gna.gna_normal.models import (
    Player,
    DailyAccessLog,
    PaymentInfo,
)
# from gna.models import (
#     TodayAccessTmp,
#     RegisterUser1Tmp,
#     RegisterUser2Tmp,
#     RegisterUser3Tmp,
#     RegisterUser4Tmp,
#     RegisterUser5Tmp,
#     RegisterUser6Tmp,
#     RegisterUser7Tmp,
#     RegisterUser14Tmp,
#     RegisterUser30Tmp,
#     RegisterUser60Tmp,
#     RegisterUser90Tmp,
# )
from gna.cache import (
    daily_cache,
    simple_cache,
    delta_cache,
    daily_flag_cache,
)

class job_base(object):
    paraments = {'delta_cache':[], 'daily_cache':[]} # do_job的参数
    depends = [] # 该job执行需要依赖其他的jobs
    action = 'inc' # do_job的结果处理，inc:再原有基础上递增，replace:替代原有值
    is_special = False # 执行的job需要的数据不在上面的参数中，需要特殊处理

    def do_job(self):
        return 0
    def do_month_job(self):
        return 0


##### 流水 #####
class income_job(job_base):
    paraments = {'delta_cache':['TABLE_PAYMENTINFO_CACHE'], 'daily_cache':[]}

    def do_job(self, datas):
        count = 0
        for data in datas:
            if data['status'] == '2':
                count += int(data['point'])
        return count


##### DAU #####
class dau_job(job_base):
    paraments = {'delta_cache':['TABLE_DAILYACCESSLOG_CACHE'], 'daily_cache':[]}

    def do_job(self, datas):
        count = len(datas)
        return count


##### ARPU(流水/DAU) #####
class arpu_job(job_base):
    paraments = {'delta_cache':[], 'daily_cache':['income', 'dau']}
    depends = ['income_job', 'dau_job']
    action = 'replace'

    def do_job(self, income_value, dau_value):
        return div_operation(income_value, dau_value)
    def do_month_job(self, income_value, dau_value):
        return self.do_job(income_value, dau_value)


##### ARPPU(流水/购买人数) #####
class arppu_job(job_base):
    paraments = {'delta_cache':[], 'daily_cache':['income', 'pay_user']}
    depends = ['income_job', 'pay_user_job']
    action = 'replace'

    def do_job(self, income_value, pay_user_value):
        return div_operation(income_value, pay_user_value)
    def do_month_job(self, income_value, pay_user_value):
        return self.do_job(income_value, pay_user_value)


##### 购买率(购买人数/DAU) #####
class pay_ratio_job(job_base):
    paraments = {'delta_cache':[], 'daily_cache':['pay_user', 'dau']}
    depends = ['pay_user_job', 'dau_job']
    action = 'replace'

    def do_job(self, pay_user_value, dau_value):
        return div_operation(pay_user_value, dau_value)
    def do_month_job(self, pay_user_value, dau_value):
        return self.do_job(pay_user_value, dau_value)


##### 购买人数 #####
class pay_user_job(job_base):
    paraments = {'delta_cache':['TABLE_PAYMENTINFO_CACHE'], 'daily_cache':[]}

    def do_job(self, datas):
        user_set = set()
        for data in datas:
            if data['status'] == '2':
                user_set.add(data['osuser_id'])
        return len(user_set)


##### 初次购买人数 #####
class first_pay_user_job(job_base):
    is_special = True

    def do_job(self, db, pre_datetime_bound, cur_datetime_bound):
        old_pay_user_set = set()
        datas = PaymentInfo.objects.using(db).filter(
                created_at__lt=pre_datetime_bound,
                status = '2',
            ).values_list('osuser_id', flat=True)
        for user in datas:
            old_pay_user_set.add(user)

        new_pay_user_set = set()
        datas = PaymentInfo.objects.using(db).filter(
                created_at__range=(pre_datetime_bound, cur_datetime_bound),
                status = '2',
            ).values_list('osuser_id', flat=True)
        for user in datas:
            new_pay_user_set.add(user)

        first_pay_user_set = new_pay_user_set - old_pay_user_set
        return len(first_pay_user_set)


##### 初次购买率(初次购买人数/购买人数) #####
class first_pay_ratio_job(job_base):
    paraments = {'delta_cache':[], 'daily_cache':['first_pay_user', 'pay_user']}
    depends = ['first_pay_user_job', 'pay_user_job']
    action = 'replace'

    def do_job(self, first_pay_user_value, pay_user_value):
        return div_operation(first_pay_user_value, pay_user_value)
    def do_month_job(self, first_pay_user_value, pay_user_value):
        return self.do_job(first_pay_user_value, pay_user_value)


##### 新注册用户 ##### 
class register_user_job(job_base):
    paraments = {'delta_cache':['TABLE_PLAYER_CACHE'], 'daily_cache':[]}

    def do_job(self, datas):
        return len(datas)


##### 留存率(1-7,14,30,60,90) #####
#----------------------------------------------------------------------------
# 实时跑的retention
#----------------------------------------------------------------------------
# @transaction.commit_manually
# class retention_ratio_job(job_base):
#     is_special = True
#     action = 'pass'
#     depends = ['register_user_job', 'dau_job']
#     days_list = settings.GNA_RETENTION_DAYS_LIST

#     def do_job(self, db, pre_datetime_bound, cur_datetime_bound):
#         days_list = settings.GNA_RETENTION_DAYS_LIST
#         the_date = pre_datetime_bound.date()

#         # 如果这是今天第一次执行，那将所有临时表清空，并更新前x天注册用户临时表
#         if date_to_datetime_begin(pre_datetime_bound.date()) == pre_datetime_bound:
#             print 'a new day'
#             for days in days_list:
#                 model_name = 'RegisterUser%dTmp'%days
#                 eval(model_name).objects.using(db).all().delete()

#                 pre_date = the_date - datetime.timedelta(days=days)

#                 created_user_set = set()
#                 query_data = Player.objects.using(db).filter(
#                         created_at__range = (date_to_datetime_begin(pre_date), date_to_datetime_end(pre_date))
#                     ).values_list('osuser_id', flat=True)

#                 for data in query_data:
#                     created_user_set.add(data)

#                 for uid in created_user_set:
#                     obj = eval(model_name)(osuser_id=uid)
#                     obj.save(using=db)
#                 transaction.commit(using=db)

#         # 获取pre与cur之间的用户
#         access_user_set = set()
#         query_data = DailyAccessLog.objects.using(db).filter(
#                 accessed_at__range = (pre_datetime_bound, cur_datetime_bound)
#             ).values_list('osuser_id', flat=True)
#         for data in query_data:
#             access_user_set.add(data)
        
#         # 统计x天留存率
#         for days in days_list:
#             model_name = 'RegisterUser%dTmp'%days
#             pre_date = the_date - datetime.timedelta(days=days)

#             created_user_set = set()
#             query_data = eval(model_name).objects.using(db).all().values_list('osuser_id', flat=True)
#             for data in query_data:
#                 created_user_set.add(data)

#             cache_key = get_retention_cache_key('retention_ratio', days)
#             retention_user_count = len(access_user_set & created_user_set)
#             created_user_count = len(created_user_set)
#             result = '%.2f%%(%d/%d)' % (100*div_operation(retention_user_count, created_user_count), retention_user_count, created_user_count)
#             daily_cache().set(db, cache_key, pre_date, result)
#----------------------------------------------------------------------------

#----------------------------------------------------------------------------
# 每天跑一次的retention
#----------------------------------------------------------------------------
class retention_ratio_job(job_base):
    is_special = True
    action = 'pass'
    depends = ['register_user_job', 'dau_job']
    days_list = settings.GNA_RETENTION_DAYS_LIST

    def do_job(self, db, pre_datetime_bound, cur_datetime_bound):
        if pre_datetime_bound.date() == cur_datetime_bound.date():
            return 0
        else:
            the_date = pre_datetime_bound.date()

        activity_user_set = set()
        query_data = DailyAccessLog.objects.using(db).filter(
                accessed_at__range = (date_to_datetime_begin(the_date), date_to_datetime_end(the_date))
            ).values_list('osuser_id', flat=True)
        for user in query_data:
            activity_user_set.add(user)

        for days in self.days_list:
            cache_key = get_retention_cache_key('retention_ratio', days)
            pre_date = the_date - datetime.timedelta(days=days)

            created_user_set = set()
            query_data = Player.objects.using(db).filter(
                    created_at__range = (date_to_datetime_begin(pre_date), date_to_datetime_end(pre_date))
                ).values_list('osuser_id', flat=True)
            for user in query_data:
                created_user_set.add(user)

            retention_user_count = len(activity_user_set & created_user_set)
            created_user_count = len(created_user_set)
            result = '%.2f%%(%d/%d)' % (100*div_operation(retention_user_count, created_user_count), retention_user_count, created_user_count)
            daily_cache().set(db, cache_key, the_date, result)

#----------------------------------------------------------------------------


# 对job处理顺序进行排序，被依赖的job先处理 
JOBS_LIST = []
JOBS_DEPENDS_LIST = []
for key, value in locals().items():
    if key.endswith('_job'):
        JOBS_LIST.append(key)
        for depend in value().depends:
            JOBS_DEPENDS_LIST.append((depend, key))

JOBS_LIST = topo_sort(JOBS_LIST, JOBS_DEPENDS_LIST)
JOBS_LIST = map(eval, JOBS_LIST)


