# -*- coding: utf-8 -*-

from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.shortcuts import render_to_response, redirect
from django.template import RequestContext

from django.conf import settings

import datetime
import math

from gna.common import (
    str_to_date,
    date_range,
    get_start_date,
    get_retention_cache_key,
    date_to_month_begin,
    get_pre_month,
    get_delta_months,
    get_delta_months_value,
    paginator,
)
from gna.api import (
    get_gna_objs_list,
    get_gna_month_obj,
    get_retention_ratio_daily_objs_list,
    get_retention_ratio_daily_objs_list_2,
)

##### list #####
@login_required
def gna_list(request, dbs=settings.GNA_DATABASES):
    date = datetime.date.today()

    page_limit = settings.GNA_WEB_LIST_DAILY_LIMIT

    # result = [{'title':db, 'head':item_name, 'body':[item_value,]}, ]
    daily_result = _get_daily_list(date, dbs)
    month_result = _get_month_list(date, dbs)
    
    result = daily_result
    for i in range(len(result)):
        result[i]['body'].extend(month_result[i]['body'])

    ctxt = RequestContext(request, {
        'result': result,
    })
    return render_to_response('gna/gna_list.html', ctxt)

@login_required
def gna_retention_list(request, dbs=settings.GNA_DATABASES):
    date = datetime.date.today() - datetime.timedelta(days=1)

    page_limit = settings.GNA_WEB_LIST_DAILY_LIMIT

    result = _get_retention_daily_list(date, dbs)
    
    ctxt = RequestContext(request, {
        'result': result,
    })
    return render_to_response('gna/gna_retention_list.html', ctxt)


##### detail #####
@login_required
def gna_daily_detail(request, db, page=1):
    if db not in settings.GNA_DATABASES:
        return render_to_response('gna/gna_daily_detail.html', RequestContext(request))

    date = datetime.date.today()

    page = int(page)
    records_num = (date - get_start_date(db)).days + 1
    limit = settings.GNA_WEB_DETAIL_DAILY_LIMIT
    page_num = int(math.ceil(records_num*1.0/limit))
    if page > page_num:
        page = page_num

    cur_page_date = date - datetime.timedelta(days=limit*(page-1))
    result = _get_daily_list(cur_page_date, [db], limit)
    
    pager = paginator(page_num, page)
    pager['url'] = reverse('gna/daily/detail', args=[db, ]) + 'page/'

    ctxt = RequestContext(request, {
        'db': result[0],
        'pager': pager,
    })
    return render_to_response('gna/gna_daily_detail.html', ctxt)

@login_required
def gna_month_detail(request, db, page=1):
    if db not in settings.GNA_DATABASES:
        return render_to_response('gna/gna_month_detail.html', RequestContext(request))

    date = datetime.date.today()

    page = int(page)
    records_num = get_delta_months_value(date, get_start_date(db)) + 1
    limit = settings.GNA_WEB_DETAIL_MONTH_LIMIT
    page_num = int(math.ceil(records_num*1.0/limit))
    if page > page_num:
        page = page_num

    cur_page_date = get_delta_months(date, -limit*(page-1)).date()
    result = _get_month_list(cur_page_date, [db], limit)

    pager = paginator(page_num, page)
    pager['url'] = reverse('gna/month/detail', args=[db, ]) + 'page/'

    ctxt = RequestContext(request, {
        'db': result[0],
        'pager': pager,
    })
    return render_to_response('gna/gna_month_detail.html', ctxt)

@login_required
def gna_retention_daily_detail(request, db, page=1):
    if db not in settings.GNA_DATABASES:
        return render_to_response('gna/gna_retention_daily_detail.html', RequestContext(request))

    date = datetime.date.today() - datetime.timedelta(days=1)

    page = int(page)
    records_num = (date - get_start_date(db)).days + 1
    limit = settings.GNA_WEB_DETAIL_DAILY_LIMIT
    page_num = int(math.ceil(records_num*1.0/limit))
    if page > page_num:
        page = page_num

    cur_page_date = date - datetime.timedelta(days=limit*(page-1))
    result = _get_retention_daily_list(cur_page_date, [db], limit)
    
    pager = paginator(page_num, page)
    pager['url'] = reverse('gna/retention/daily/detail', args=[db, ]) + 'page/'

    ctxt = RequestContext(request, {
        'db': result[0],
        'pager': pager,
    })
    return render_to_response('gna/gna_retention_daily_detail.html', ctxt)

##### get_list #####
def _get_daily_list(date, dbs, page_limit=settings.GNA_WEB_LIST_DAILY_LIMIT):
    # result = [{'title':db, 'head':item_name, 'body':[item_value,]}, ]
    result = []
    for db in dbs:
        result_row = {'db':db, 'title':settings.GNA_DATABASE_NAME[db], 'head':[], 'body':[]}
        result_row['head'] = ['日期', '流水', '登录角色数', 'ARPU', 'ARPPU', '购买人数', '购买率', '初次购买人数', '初次购买率', '新建角色数']

        date_begin = max(date-datetime.timedelta(days=page_limit-1), get_start_date(db))
        if date_begin > date:
            continue

        objs = get_gna_objs_list(db, date_begin, date)

        for obj in objs:
            body_row = [obj.date_str, ]
            body_row.append(obj.income_str)
            body_row.append(obj.dau_str)
            body_row.append(obj.arpu_str)
            body_row.append(obj.arppu_str)
            body_row.append(obj.pay_user_str)
            body_row.append(obj.pay_ratio_str)
            body_row.append(obj.first_pay_user_str)
            body_row.append(obj.first_pay_ratio_str)
            body_row.append(obj.register_user_str)

            result_row['body'].append(body_row)

        result.append(result_row)

    return result

def _get_month_list(date, dbs, page_limit=settings.GNA_WEB_LIST_MONTH_LIMIT):
    # result = [{'title':db, 'head':item_name, 'body':[item_value,]}, ]
    result = []
    for db in dbs:
        result_row = {'db':db, 'title':settings.GNA_DATABASE_NAME[db], 'head':[], 'body':[]}
        result_row['head'] = ['日期', '流水', '登录角色数', 'ARPU', 'ARPPU', '购买人数', '购买率', '初次购买人数', '初次购买率', '新建角色数']

        date_list = []
        global_start_date = date_to_month_begin(get_start_date(db)).date()
        the_date = date
        for i in range(page_limit):
            if the_date < global_start_date:
                break
            date_list.append(the_date)
            the_date = get_pre_month(the_date).date()
        
        if not date_list:
            continue

        for the_date in date_list:
            obj = get_gna_month_obj(db, the_date)
            body_row = [the_date.strftime('%Y-%m'),]
            body_row.append(obj.income_str)
            body_row.append(obj.dau_str)
            body_row.append(obj.arpu_str)
            body_row.append(obj.arppu_str)
            body_row.append(obj.pay_user_str)
            body_row.append(obj.pay_ratio_str)
            body_row.append(obj.first_pay_user_str)
            body_row.append(obj.first_pay_ratio_str)
            body_row.append(obj.register_user_str)

            result_row['body'].append(body_row)

        result.append(result_row)

    return result

def _get_retention_daily_list(date, dbs, page_limit=settings.GNA_WEB_LIST_DAILY_LIMIT):
    days_list = settings.GNA_RETENTION_DAYS_LIST
    result = []
    for db in dbs:
        result_row = {'db':db, 'title':settings.GNA_DATABASE_NAME[db], 'head':[], 'body':[]}

        result_row['head'].append('日期')
        for days in days_list:
            result_row['head'].append('%d日留存率'%days)

        date_begin = max(date-datetime.timedelta(days=page_limit-1), get_start_date(db))
        if date_begin > date:
            continue

        objs = get_retention_ratio_daily_objs_list_2(db, date_begin, date)

        for obj in objs:
            body_row = [obj.date_str, ]

            for days in days_list:
                body_row.append(getattr(obj, 'retention_ratio%d_str'%days))

            result_row['body'].append(body_row)

        result.append(result_row)

    return result

