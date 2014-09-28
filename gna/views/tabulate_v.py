# -*- coding: utf-8 -*-
from django.contrib.auth.decorators import login_required
from django.shortcuts import render_to_response
from django.views.decorators.csrf import csrf_protect
from django.template import RequestContext
from django.core.urlresolvers import reverse 
from django.conf import settings

import datetime
import math

from gna.common import (
    str_to_date,
    date_to_str,
    date_range,
    get_start_date,
    get_retention_cache_key,
    date_to_month_begin,
    get_pre_month,
    get_delta_months,
    get_delta_months_value,
    paginator,
)
from gna.tabulate.api import (
    get_date_count_objs_list,
    get_date_platform_count_objs_list,
    get_platform_date_count_objs_list,
    get_date_channel_count_objs_list,
    get_channel_date_count_objs_list,
)

@login_required
def tabulate_home(request):
    ctxt = RequestContext(request, {})
    return render_to_response('gna/tabulate/home.html')

@login_required
def daily_date(request, page=1):
    dbs = settings.TABULATE_DATABASE
    db = dbs[0]
    date = datetime.date.today() - datetime.timedelta(days=1)
    
    # paginator
    page = int(page)
    records_num = (date - get_start_date(db)).days + 1
    limit = settings.TABULATE_WEB_LIST_DAILY_DATE_LIMIT
    page_num = int(math.ceil(records_num*1.0/limit))
    if page > page_num:
        page = page_num

    cur_page_date = date - datetime.timedelta(days=limit*(page-1))
        # result
    result = _get_daily_date_list(cur_page_date, [db], limit)
    
    pager = paginator(page_num, page)
    pager['url'] = reverse('tabulate/daily_date') + 'page/'

    ctxt = RequestContext(request, {
        'result': result,
        'selected': {'daily_date': True},
        'pager': pager,
    })
    return render_to_response('gna/tabulate/daily_date.html', ctxt)

@login_required
@csrf_protect
def daily_date_platform(request):
    date = request.REQUEST.get('request_date')
    # warning (verify date)
    warning = None
    try:
        date = str_to_date(date)        
    except:
        if date:
            warning = {'text': '日期格式错误'}
        date = datetime.date.today() - datetime.timedelta(days=1)

    dbs = settings.TABULATE_DATABASE

    # result
    result = _get_daily_date_platform_list(date, dbs)

    ctxt = RequestContext(request, {
        'result': result,
        'selected': {'daily_date_platform': True},
        'warning': warning,
        'date_str': date_to_str(date),
    })
    return render_to_response('gna/tabulate/daily_date_platform.html', ctxt)

@login_required
@csrf_protect
def daily_platform_date(request, platform=settings.TABULATE_PLATFORM_LIST[0], page=1):
    dbs = settings.TABULATE_DATABASE
    db = dbs[0]
    date = datetime.date.today() - datetime.timedelta(days=1)
    
    # platform selected
    platform_selected = int(platform)
    if platform_selected not in settings.TABULATE_PLATFORM_LIST:
        try:
            platform_selected = request.REQUEST.get('select_platform')
            platform_selected = int(platform_selected)
            if platform_selected not in settings.TABULATE_PLATFORM_LIST:
                platform_selected = settings.TABULATE_PLATFORM_LIST[0]
        except:
            platform_selected = settings.TABULATE_PLATFORM_LIST[0]
    
    # choices
    platform_list = settings.TABULATE_PLATFORM_LIST
    choices = []
    for platform in platform_list:
        choices.append({'id': platform, 'name': settings.TABULATE_PLATFORM_NAME[platform], 'selected': True if platform==platform_selected else False})

    # paginator
    page = int(page)
    records_num = (date - get_start_date(db)).days + 1
    limit = settings.TABULATE_WEB_LIST_DAILY_PLATFORM_DATE_LIMIT
    page_num = int(math.ceil(records_num*1.0/limit))
    if page > page_num:
        page = page_num

    cur_page_date = date - datetime.timedelta(days=limit*(page-1))
        # result
    result = _get_daily_platform_date_list(cur_page_date, platform_selected, [db], limit)
    
    pager = paginator(page_num, page)
    pager['url'] = reverse('tabulate/daily_platform_date/platform', args=[str(platform_selected), ]) + 'page/'

    ctxt = RequestContext(request, {
        'result': result,
        'selected': {'daily_platform_date': True},
        'choices': choices,
        'pager': pager,
        'url_args': {'platform': platform_selected, 'page': page},
    })
    return render_to_response('gna/tabulate/daily_platform_date.html', ctxt)

@login_required
@csrf_protect
def daily_date_channel(request):
    date = request.REQUEST.get('request_date')
    # warning (verify date)
    warning = None
    try:
        date = str_to_date(date)        
    except:
        if date:
            warning = {'text': '日期格式错误'}
        date = datetime.date.today() - datetime.timedelta(days=1)

    dbs = settings.TABULATE_DATABASE

    # result
    result = _get_daily_date_channel_list(date, dbs)

    ctxt = RequestContext(request, {
        'result': result,
        'selected': {'daily_date_channel': True},
        'warning': warning,
        'date_str': date_to_str(date),
    })
    return render_to_response('gna/tabulate/daily_date_channel.html', ctxt)

@login_required
@csrf_protect
def daily_channel_date(request, channel=settings.TABULATE_CHANNEL_LIST[0], page=1):
    dbs = settings.TABULATE_DATABASE
    db = dbs[0]
    date = datetime.date.today() - datetime.timedelta(days=1)
    
    # channel selected
    channel_selected = channel
    if channel_selected not in settings.TABULATE_CHANNEL_LIST:
        try:
            channel_selected = request.REQUEST.get('select_channel')
            if channel_selected not in settings.TABULATE_CHANNEL_LIST:
                channel_selected = settings.TABULATE_CHANNEL_LIST[0]
        except:
            channel_selected = settings.TABULATE_CHANNEL_LIST[0]
    
    # choices
    channel_list = settings.TABULATE_CHANNEL_LIST
    choices = []
    for channel in channel_list:
        choices.append({'id': channel, 'name': settings.TABULATE_CHANNEL_NAME[channel], 'selected': True if channel==channel_selected else False})

    # paginator
    page = int(page)
    records_num = (date - get_start_date(db)).days + 1
    limit = settings.TABULATE_WEB_LIST_DAILY_CHANNEL_DATE_LIMIT
    page_num = int(math.ceil(records_num*1.0/limit))
    if page > page_num:
        page = page_num

    cur_page_date = date - datetime.timedelta(days=limit*(page-1))
        # result
    result = _get_daily_channel_date_list(cur_page_date, channel_selected, [db], limit)
    
    pager = paginator(page_num, page)
    pager['url'] = reverse('tabulate/daily_channel_date/channel', args=[str(channel_selected), ]) + 'page/'

    ctxt = RequestContext(request, {
        'result': result,
        'selected': {'daily_channel_date': True},
        'choices': choices,
        'pager': pager,
        'url_args': {'channel': channel_selected, 'page': page},
    })
    return render_to_response('gna/tabulate/daily_channel_date.html', ctxt)

##### get_list #####
def _get_daily_date_list(date, dbs, page_limit=settings.TABULATE_WEB_LIST_DAILY_DATE_LIMIT):
    result = []
    for db in dbs:
        result_db = {}
        result_db['title'] = '每日汇总数据'
        result_db['head'] = [
            {'value': '日期'},
        ] + _get_name_list()
        result_db['body'] = []
        date_begin = max(date-datetime.timedelta(days=page_limit-1), get_start_date(db))
        if date_begin > date:
            continue

        objs = get_date_count_objs_list(db, date_begin, date)

        objs = _filter_objs_value_all_none(objs)

        for obj in objs:
            body_row = [{'is_red':False, 'value':_get_date_str(obj.date)}, ]
            body_row.append({'is_red':False, 'value':obj.device_count_str})
            body_row.append({'is_red':False, 'value':obj.user_count_str})
            body_row.append({'is_red':False, 'value':obj.user_login_str})
            body_row.append({'is_red':False, 'value':obj.dau_str})
            body_row.append({'is_red':False, 'value':obj.vip_count_str})
            body_row.append({'is_red':False, 'value':obj.vip_amount_str})
            body_row.append({'is_red':True if obj.vip_ratio>settings.TABULATE_FILTER_VIP_RATIO_GT else False, 'value':obj.vip_ratio_str})
            body_row.append({'is_red':True if obj.arppu>settings.TABULATE_FILTER_ARPPU_GT else False, 'value':obj.arppu_str})
            body_row.append({'is_red':False, 'value':obj.purchase_suc_ratio_str})
            body_row.append({'is_red':True if obj.lc1_ratio>settings.TABULATE_FILTER_LC1_RATIO_GT else False, 'value':obj.lc1_ratio_str})
            body_row.append({'is_red':True if obj.lc2_ratio>settings.TABULATE_FILTER_LC2_RATIO_GT else False, 'value':obj.lc2_ratio_str})
            body_row.append({'is_red':True if obj.lc3_ratio>settings.TABULATE_FILTER_LC3_RATIO_GT else False, 'value':obj.lc3_ratio_str})
            body_row.append({'is_red':True if obj.lc4_ratio>settings.TABULATE_FILTER_LC4_RATIO_GT else False, 'value':obj.lc4_ratio_str})
            body_row.append({'is_red':True if obj.lc5_ratio>settings.TABULATE_FILTER_LC5_RATIO_GT else False, 'value':obj.lc5_ratio_str})
            body_row.append({'is_red':True if obj.lc6_ratio>settings.TABULATE_FILTER_LC6_RATIO_GT else False, 'value':obj.lc6_ratio_str})
            body_row.append({'is_red':True if obj.lc7_ratio>settings.TABULATE_FILTER_LC7_RATIO_GT else False, 'value':obj.lc7_ratio_str})
            body_row.append({'is_red':True if obj.lc14_ratio>settings.TABULATE_FILTER_LC14_RATIO_GT else False, 'value':obj.lc14_ratio_str})
            body_row.append({'is_red':True if obj.lc30_ratio>settings.TABULATE_FILTER_LC30_RATIO_GT else False, 'value':obj.lc30_ratio_str})

            result_db['body'].append(body_row)

        result.append(result_db)
    return result

def _get_daily_date_platform_list(date, dbs, page_limit=settings.TABULATE_WEB_LIST_DAILY_DATE_PLATFORM_LIMIT):
    result = []
    for db in dbs:
        result_db = {}
        result_db['title'] = '每日各平台汇总数据'
        result_db['head'] = [
            {'value': '日期'}, 
            {'value': '平台', 'width': 110},
        ] + _get_name_list()
        result_db['body'] = []

        objs = get_date_platform_count_objs_list(db, date, settings.TABULATE_PLATFORM_LIST)

        objs = _filter_objs_value_all_none(objs)

        for obj in objs:
            body_row = [{'is_red':False, 'value':_get_date_str(obj.date)}, ]
            body_row.append({'is_red':False, 'value':settings.TABULATE_PLATFORM_NAME[obj.platform]})
            body_row.append({'is_red':False, 'value':obj.device_count_str})
            body_row.append({'is_red':False, 'value':obj.user_count_str})
            body_row.append({'is_red':False, 'value':obj.user_login_str})
            body_row.append({'is_red':False, 'value':obj.dau_str})
            body_row.append({'is_red':False, 'value':obj.vip_count_str})
            body_row.append({'is_red':False, 'value':obj.vip_amount_str})
            body_row.append({'is_red':True if obj.vip_ratio>settings.TABULATE_FILTER_VIP_RATIO_GT else False, 'value':obj.vip_ratio_str})
            body_row.append({'is_red':True if obj.arppu>settings.TABULATE_FILTER_ARPPU_GT else False, 'value':obj.arppu_str})
            body_row.append({'is_red':False, 'value':obj.purchase_suc_ratio_str})
            body_row.append({'is_red':True if obj.lc1_ratio>settings.TABULATE_FILTER_LC1_RATIO_GT else False, 'value':obj.lc1_ratio_str})
            body_row.append({'is_red':True if obj.lc2_ratio>settings.TABULATE_FILTER_LC2_RATIO_GT else False, 'value':obj.lc2_ratio_str})
            body_row.append({'is_red':True if obj.lc3_ratio>settings.TABULATE_FILTER_LC3_RATIO_GT else False, 'value':obj.lc3_ratio_str})
            body_row.append({'is_red':True if obj.lc4_ratio>settings.TABULATE_FILTER_LC4_RATIO_GT else False, 'value':obj.lc4_ratio_str})
            body_row.append({'is_red':True if obj.lc5_ratio>settings.TABULATE_FILTER_LC5_RATIO_GT else False, 'value':obj.lc5_ratio_str})
            body_row.append({'is_red':True if obj.lc6_ratio>settings.TABULATE_FILTER_LC6_RATIO_GT else False, 'value':obj.lc6_ratio_str})
            body_row.append({'is_red':True if obj.lc7_ratio>settings.TABULATE_FILTER_LC7_RATIO_GT else False, 'value':obj.lc7_ratio_str})
            body_row.append({'is_red':True if obj.lc14_ratio>settings.TABULATE_FILTER_LC14_RATIO_GT else False, 'value':obj.lc14_ratio_str})
            body_row.append({'is_red':True if obj.lc30_ratio>settings.TABULATE_FILTER_LC30_RATIO_GT else False, 'value':obj.lc30_ratio_str})

            result_db['body'].append(body_row)

        result.append(result_db)
    return result

def _get_daily_platform_date_list(date, platform, dbs, page_limit=settings.TABULATE_WEB_LIST_DAILY_PLATFORM_DATE_LIMIT):
    result = []
    for db in dbs:
        result_db = {}
        result_db['title'] = '各平台每日汇总数据'
        result_db['head'] = [
            {'value': '日期'}, 
            {'value': '平台', 'width': 110},
        ] + _get_name_list()
        result_db['body'] = []

        date_begin = max(date-datetime.timedelta(days=page_limit-1), get_start_date(db))
        if date_begin > date:
            continue

        objs = get_platform_date_count_objs_list(db, date_begin, date, platform)

        objs = _filter_objs_value_all_none(objs)

        for obj in objs:
            body_row = [{'is_red':False, 'value':_get_date_str(obj.date)}, ]
            body_row.append({'is_red':False, 'value':settings.TABULATE_PLATFORM_NAME[obj.platform]})
            body_row.append({'is_red':False, 'value':obj.device_count_str})
            body_row.append({'is_red':False, 'value':obj.user_count_str})
            body_row.append({'is_red':False, 'value':obj.user_login_str})
            body_row.append({'is_red':False, 'value':obj.dau_str})
            body_row.append({'is_red':False, 'value':obj.vip_count_str})
            body_row.append({'is_red':False, 'value':obj.vip_amount_str})
            body_row.append({'is_red':True if obj.vip_ratio>settings.TABULATE_FILTER_VIP_RATIO_GT else False, 'value':obj.vip_ratio_str})
            body_row.append({'is_red':True if obj.arppu>settings.TABULATE_FILTER_ARPPU_GT else False, 'value':obj.arppu_str})
            body_row.append({'is_red':False, 'value':obj.purchase_suc_ratio_str})
            body_row.append({'is_red':True if obj.lc1_ratio>settings.TABULATE_FILTER_LC1_RATIO_GT else False, 'value':obj.lc1_ratio_str})
            body_row.append({'is_red':True if obj.lc2_ratio>settings.TABULATE_FILTER_LC2_RATIO_GT else False, 'value':obj.lc2_ratio_str})
            body_row.append({'is_red':True if obj.lc3_ratio>settings.TABULATE_FILTER_LC3_RATIO_GT else False, 'value':obj.lc3_ratio_str})
            body_row.append({'is_red':True if obj.lc4_ratio>settings.TABULATE_FILTER_LC4_RATIO_GT else False, 'value':obj.lc4_ratio_str})
            body_row.append({'is_red':True if obj.lc5_ratio>settings.TABULATE_FILTER_LC5_RATIO_GT else False, 'value':obj.lc5_ratio_str})
            body_row.append({'is_red':True if obj.lc6_ratio>settings.TABULATE_FILTER_LC6_RATIO_GT else False, 'value':obj.lc6_ratio_str})
            body_row.append({'is_red':True if obj.lc7_ratio>settings.TABULATE_FILTER_LC7_RATIO_GT else False, 'value':obj.lc7_ratio_str})
            body_row.append({'is_red':True if obj.lc14_ratio>settings.TABULATE_FILTER_LC14_RATIO_GT else False, 'value':obj.lc14_ratio_str})
            body_row.append({'is_red':True if obj.lc30_ratio>settings.TABULATE_FILTER_LC30_RATIO_GT else False, 'value':obj.lc30_ratio_str})

            result_db['body'].append(body_row)

        result.append(result_db)
    return result 

def _get_daily_date_channel_list(date, dbs, page_limit=settings.TABULATE_WEB_LIST_DAILY_DATE_CHANNEL_LIMIT):
    result = []
    for db in dbs:
        result_db = {}
        result_db['title'] = '每日各渠道汇总数据'
        result_db['head'] = [
            {'value': '日期'}, 
            {'value': '渠道', 'width': 110},
        ] + _get_name_list()        
        result_db['body'] = []

        objs = get_date_channel_count_objs_list(db, date, settings.TABULATE_CHANNEL_LIST)

        objs = _filter_objs_value_all_none(objs)

        objs.reverse()

        objs.sort(key=lambda x: x.dau, reverse=True)

        for obj in objs:
            body_row = [{'is_red':False, 'value':_get_date_str(obj.date)}, ]
            body_row.append({'is_red':False, 'value':settings.TABULATE_CHANNEL_NAME[obj.channel]})
            body_row.append({'is_red':False, 'value':obj.device_count_str})
            body_row.append({'is_red':False, 'value':obj.user_count_str})
            body_row.append({'is_red':False, 'value':obj.user_login_str})
            body_row.append({'is_red':False, 'value':obj.dau_str})
            body_row.append({'is_red':False, 'value':obj.vip_count_str})
            body_row.append({'is_red':False, 'value':obj.vip_amount_str})
            body_row.append({'is_red':True if obj.vip_ratio>settings.TABULATE_FILTER_VIP_RATIO_GT else False, 'value':obj.vip_ratio_str})
            body_row.append({'is_red':True if obj.arppu>settings.TABULATE_FILTER_ARPPU_GT else False, 'value':obj.arppu_str})
            body_row.append({'is_red':False, 'value':obj.purchase_suc_ratio_str})
            body_row.append({'is_red':True if obj.lc1_ratio>settings.TABULATE_FILTER_LC1_RATIO_GT else False, 'value':obj.lc1_ratio_str})
            body_row.append({'is_red':True if obj.lc2_ratio>settings.TABULATE_FILTER_LC2_RATIO_GT else False, 'value':obj.lc2_ratio_str})
            body_row.append({'is_red':True if obj.lc3_ratio>settings.TABULATE_FILTER_LC3_RATIO_GT else False, 'value':obj.lc3_ratio_str})
            body_row.append({'is_red':True if obj.lc4_ratio>settings.TABULATE_FILTER_LC4_RATIO_GT else False, 'value':obj.lc4_ratio_str})
            body_row.append({'is_red':True if obj.lc5_ratio>settings.TABULATE_FILTER_LC5_RATIO_GT else False, 'value':obj.lc5_ratio_str})
            body_row.append({'is_red':True if obj.lc6_ratio>settings.TABULATE_FILTER_LC6_RATIO_GT else False, 'value':obj.lc6_ratio_str})
            body_row.append({'is_red':True if obj.lc7_ratio>settings.TABULATE_FILTER_LC7_RATIO_GT else False, 'value':obj.lc7_ratio_str})
            body_row.append({'is_red':True if obj.lc14_ratio>settings.TABULATE_FILTER_LC14_RATIO_GT else False, 'value':obj.lc14_ratio_str})
            body_row.append({'is_red':True if obj.lc30_ratio>settings.TABULATE_FILTER_LC30_RATIO_GT else False, 'value':obj.lc30_ratio_str})

            result_db['body'].append(body_row)

        result.append(result_db)
    return result

def _get_daily_channel_date_list(date, channel, dbs, page_limit=settings.TABULATE_WEB_LIST_DAILY_CHANNEL_DATE_LIMIT):
    result = []
    for db in dbs:
        result_db = {}
        result_db['title'] = '各渠道每日汇总数据'
        result_db['head'] = [
            {'value': '日期'}, 
            {'value': '渠道', 'width': 110},
        ] + _get_name_list()
        result_db['body'] = []

        date_begin = max(date-datetime.timedelta(days=page_limit-1), get_start_date(db))
        if date_begin > date:
            continue

        objs = get_channel_date_count_objs_list(db, date_begin, date, channel)

        objs = _filter_objs_value_all_none(objs)

        for obj in objs:
            body_row = [{'is_red':False, 'value':_get_date_str(obj.date)}, ]
            body_row.append({'is_red':False, 'value':settings.TABULATE_CHANNEL_NAME[obj.channel]})
            body_row.append({'is_red':False, 'value':obj.device_count_str})
            body_row.append({'is_red':False, 'value':obj.user_count_str})
            body_row.append({'is_red':False, 'value':obj.user_login_str})
            body_row.append({'is_red':False, 'value':obj.dau_str})
            body_row.append({'is_red':False, 'value':obj.vip_count_str})
            body_row.append({'is_red':False, 'value':obj.vip_amount_str})
            body_row.append({'is_red':True if obj.vip_ratio>settings.TABULATE_FILTER_VIP_RATIO_GT else False, 'value':obj.vip_ratio_str})
            body_row.append({'is_red':True if obj.arppu>settings.TABULATE_FILTER_ARPPU_GT else False, 'value':obj.arppu_str})
            body_row.append({'is_red':False, 'value':obj.purchase_suc_ratio_str})
            body_row.append({'is_red':True if obj.lc1_ratio>settings.TABULATE_FILTER_LC1_RATIO_GT else False, 'value':obj.lc1_ratio_str})
            body_row.append({'is_red':True if obj.lc2_ratio>settings.TABULATE_FILTER_LC2_RATIO_GT else False, 'value':obj.lc2_ratio_str})
            body_row.append({'is_red':True if obj.lc3_ratio>settings.TABULATE_FILTER_LC3_RATIO_GT else False, 'value':obj.lc3_ratio_str})
            body_row.append({'is_red':True if obj.lc4_ratio>settings.TABULATE_FILTER_LC4_RATIO_GT else False, 'value':obj.lc4_ratio_str})
            body_row.append({'is_red':True if obj.lc5_ratio>settings.TABULATE_FILTER_LC5_RATIO_GT else False, 'value':obj.lc5_ratio_str})
            body_row.append({'is_red':True if obj.lc6_ratio>settings.TABULATE_FILTER_LC6_RATIO_GT else False, 'value':obj.lc6_ratio_str})
            body_row.append({'is_red':True if obj.lc7_ratio>settings.TABULATE_FILTER_LC7_RATIO_GT else False, 'value':obj.lc7_ratio_str})
            body_row.append({'is_red':True if obj.lc14_ratio>settings.TABULATE_FILTER_LC14_RATIO_GT else False, 'value':obj.lc14_ratio_str})
            body_row.append({'is_red':True if obj.lc30_ratio>settings.TABULATE_FILTER_LC30_RATIO_GT else False, 'value':obj.lc30_ratio_str})

            result_db['body'].append(body_row)

        result.append(result_db)
    return result 

def _get_name_list():
    name_list = [
        {'value': '新增设备', 'width': 45},
        {'value': '新建角色数', 'width': 45},
        {'value': '登录角色数', 'width': 45},
        {'value': 'Dau', 'width': 45},
        {'value': '付费角色数', 'width': 45},
        {'value': '付费金额', 'width': 45},
        {'value': '付费率'},
        {'value': '付费ARPPU', 'width': 55},
        {'value': '订单成功率'},
        {'value': '1日留存率'},
        {'value': '2日留存率'},
        {'value': '3日留存率'},
        {'value': '4日留存率'},
        {'value': '5日留存率'},
        {'value': '6日留存率'},
        {'value': '7日留存率'},
        {'value': '14日留存率'},
        {'value': '30日留存率'},
    ]
    return name_list

def _filter_objs_value_all_none(objs):
    tmp_objs = []
    for obj in objs:
        if not _is_obj_value_all_none(obj):
            tmp_objs.append(obj)
    return tmp_objs

def _is_obj_value_all_none(obj):
    if obj.device_count:
        return False
    if obj.user_count:
        return False
    if obj.user_login:
        return False
    if obj.dau:
        return False
    if obj.vip_count:
        return False
    if obj.vip_amount:
        return False
    if obj.vip_ratio:
        return False
    if obj.arppu:
        return False
    if obj.purchase_suc_ratio:
        return False
    if obj.lc1_ratio:
        return False
    if obj.lc2_ratio:
        return False
    if obj.lc3_ratio:
        return False
    if obj.lc4_ratio:
        return False
    if obj.lc5_ratio:
        return False
    if obj.lc6_ratio:
        return False
    if obj.lc7_ratio:
        return False
    if obj.lc14_ratio:
        return False
    if obj.lc30_ratio:
        return False
    return True

def _get_date_str(date):
    return date.strftime('%Y/%m/%d')
