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
    get_start_date,
    paginator,
)
from gna.tabulate.monitor_api import (
    get_top_vip_objs_list,
    get_top_dia_objs_list,
    get_top_zel_objs_list,
    get_top_karma_objs_list,
    get_top_vip7_objs_list,
)

# 当日充值排行榜
@login_required
@csrf_protect
def monitor_top_vip(request):
    db = settings.TABULATE_DATABASE[0]

    # date and warning (verify date)
    date = request.REQUEST.get('request_date')
    warning = None
    try:
        date = str_to_date(date)
    except:
        if date:
            warning = {'text': '日期格式错误'}
        date = datetime.date.today() - datetime.timedelta(days=1)

    # result
    result = _get_monitor_top_vip(db, date)

    ctxt = RequestContext(request, {
        'result': result,
        'warning': warning,
        'date_str': date_to_str(date),
        'selected': {'monitor_top_vip': True},
        'url': reverse('tabulate/monitor_top_vip'),
    })

    return render_to_response('gna/tabulate/monitor_show.html', ctxt)

def _get_monitor_top_vip(db, date):
    result = {}
    result['title'] = '当日充值排行榜  ' + _get_date_str(date)
    result['head'] = ['排行', '区服', '角色昵称', '充值次数', '充值金额', '等级', '渠道', '最后更新日期', '距上次更新天数']
    result['body'] = []
    
    if date < get_start_date(db):
        return

    objs = get_top_vip_objs_list(db, date)

    for obj in objs:
        body_row = [{'value':obj.rank_str}, ]
        body_row.append({'value':obj.zone_str})
        body_row.append({'value':obj.user_str})
        body_row.append({'value':obj.times_str})
        body_row.append({'value':obj.amount_str})
        body_row.append({'value':obj.lv_str})
        body_row.append({'value':obj.channel_str})
        body_row.append({'value':obj.update_date_str})
        body_row.append({'value':obj.update_day_str})

        result['body'].append(body_row)

    return result

# 钻石产出排行榜
@login_required
@csrf_protect
def monitor_top_dia_product(request):
    db = settings.TABULATE_DATABASE[0]

    # date and warning (verify date)
    date = request.REQUEST.get('request_date')
    warning = None
    try:
        date = str_to_date(date)
    except:
        if date:
            warning = {'text': '日期格式错误'}
        date = datetime.date.today() - datetime.timedelta(days=1)

    # result
    result = _get_monitor_top_dia_product(db, date, 1)

    ctxt = RequestContext(request, {
        'result': result,
        'warning': warning,
        'date_str': date_to_str(date),
        'selected': {'monitor_top_dia_product': True},
        'url': reverse('tabulate/monitor_top_dia_product'),
    })

    return render_to_response('gna/tabulate/monitor_show.html', ctxt)

def _get_monitor_top_dia_product(db, date, do_type):
    result = {}
    result['title'] = '钻石产出排行榜  ' + _get_date_str(date)
    result['head'] = ['排行', '区服', '角色昵称', '产出次数', '钻石产出数量']
    result['body'] = []
    
    if date < get_start_date(db):
        return

    objs = get_top_dia_objs_list(db, date, do_type)

    for obj in objs:
        body_row = [{'value':obj.rank_str}, ]
        body_row.append({'value':obj.zone_str})
        body_row.append({'value':obj.user_str})
        body_row.append({'value':obj.times_str})
        body_row.append({'value':obj.amount_str})

        result['body'].append(body_row)

    return result

# 钻石消耗排行榜
@login_required
@csrf_protect
def monitor_top_dia_consume(request):
    db = settings.TABULATE_DATABASE[0]

    # date and warning (verify date)
    date = request.REQUEST.get('request_date')
    warning = None
    try:
        date = str_to_date(date)
    except:
        if date:
            warning = {'text': '日期格式错误'}
        date = datetime.date.today() - datetime.timedelta(days=1)

    # result
    result = _get_monitor_top_dia_consume(db, date, 2)

    ctxt = RequestContext(request, {
        'result': result,
        'warning': warning,
        'date_str': date_to_str(date),
        'selected': {'monitor_top_dia_consume': True},
        'url': reverse('tabulate/monitor_top_dia_consume'),
    })

    return render_to_response('gna/tabulate/monitor_show.html', ctxt)

def _get_monitor_top_dia_consume(db, date, do_type):
    result = {}
    result['title'] = '钻石消耗排行榜  ' + _get_date_str(date)
    result['head'] = ['排行', '区服', '角色昵称', '消耗次数', '钻石消耗数量']
    result['body'] = []
    
    if date < get_start_date(db):
        return

    objs = get_top_dia_objs_list(db, date, do_type)

    for obj in objs:
        body_row = [{'value':obj.rank_str}, ]
        body_row.append({'value':obj.zone_str})
        body_row.append({'value':obj.user_str})
        body_row.append({'value':obj.times_str})
        body_row.append({'value':obj.amount_str})

        result['body'].append(body_row)

    return result

# 金币产出排行榜
@login_required
@csrf_protect
def monitor_top_zel_product(request):
    db = settings.TABULATE_DATABASE[0]

    # date and warning (verify date)
    date = request.REQUEST.get('request_date')
    warning = None
    try:
        date = str_to_date(date)
    except:
        if date:
            warning = {'text': '日期格式错误'}
        date = datetime.date.today() - datetime.timedelta(days=1)

    # result
    result = _get_monitor_top_zel_product(db, date, 1)

    ctxt = RequestContext(request, {
        'result': result,
        'warning': warning,
        'date_str': date_to_str(date),
        'selected': {'monitor_top_zel_product': True},
        'url': reverse('tabulate/monitor_top_zel_product'),
    })

    return render_to_response('gna/tabulate/monitor_show.html', ctxt)

def _get_monitor_top_zel_product(db, date, do_type):
    result = {}
    result['title'] = '金币产出排行榜  ' + _get_date_str(date)
    result['head'] = ['排行', '区服', '角色昵称', '产出次数', '金币产出数量']
    result['body'] = []
    
    if date < get_start_date(db):
        return

    objs = get_top_zel_objs_list(db, date, do_type)

    for obj in objs:
        body_row = [{'value':obj.rank_str}, ]
        body_row.append({'value':obj.zone_str})
        body_row.append({'value':obj.user_str})
        body_row.append({'value':obj.times_str})
        body_row.append({'value':obj.amount_str})

        result['body'].append(body_row)

    return result

# 金币消耗排行榜
@login_required
@csrf_protect
def monitor_top_zel_consume(request):
    db = settings.TABULATE_DATABASE[0]

    # date and warning (verify date)
    date = request.REQUEST.get('request_date')
    warning = None
    try:
        date = str_to_date(date)
    except:
        if date:
            warning = {'text': '日期格式错误'}
        date = datetime.date.today() - datetime.timedelta(days=1)

    # result
    result = _get_monitor_top_zel_consume(db, date, 2)

    ctxt = RequestContext(request, {
        'result': result,
        'warning': warning,
        'date_str': date_to_str(date),
        'selected': {'monitor_top_zel_consume': True},
        'url': reverse('tabulate/monitor_top_zel_consume'),
    })

    return render_to_response('gna/tabulate/monitor_show.html', ctxt)

def _get_monitor_top_zel_consume(db, date, do_type):
    result = {}
    result['title'] = '金币消耗排行榜  ' + _get_date_str(date)
    result['head'] = ['排行', '区服', '角色昵称', '消耗次数', '金币消耗数量']
    result['body'] = []
    
    if date < get_start_date(db):
        return

    objs = get_top_zel_objs_list(db, date, do_type)

    for obj in objs:
        body_row = [{'value':obj.rank_str}, ]
        body_row.append({'value':obj.zone_str})
        body_row.append({'value':obj.user_str})
        body_row.append({'value':obj.times_str})
        body_row.append({'value':obj.amount_str})

        result['body'].append(body_row)

    return result

# 魂产出排行榜
@login_required
@csrf_protect
def monitor_top_karma_product(request):
    db = settings.TABULATE_DATABASE[0]

    # date and warning (verify date)
    date = request.REQUEST.get('request_date')
    warning = None
    try:
        date = str_to_date(date)
    except:
        if date:
            warning = {'text': '日期格式错误'}
        date = datetime.date.today() - datetime.timedelta(days=1)

    # result
    result = _get_monitor_top_karma_product(db, date, 1)

    ctxt = RequestContext(request, {
        'result': result,
        'warning': warning,
        'date_str': date_to_str(date),
        'selected': {'monitor_top_karma_product': True},
        'url': reverse('tabulate/monitor_top_karma_product'),
    })

    return render_to_response('gna/tabulate/monitor_show.html', ctxt)

def _get_monitor_top_karma_product(db, date, do_type):
    result = {}
    result['title'] = '魂产出排行榜  ' + _get_date_str(date)
    result['head'] = ['排行', '区服', '角色昵称', '产出次数', '魂产出数量']
    result['body'] = []
    
    if date < get_start_date(db):
        return

    objs = get_top_karma_objs_list(db, date, do_type)

    for obj in objs:
        body_row = [{'value':obj.rank_str}, ]
        body_row.append({'value':obj.zone_str})
        body_row.append({'value':obj.user_str})
        body_row.append({'value':obj.times_str})
        body_row.append({'value':obj.amount_str})

        result['body'].append(body_row)

    return result

# 魂消耗排行榜
@login_required
@csrf_protect
def monitor_top_karma_consume(request):
    db = settings.TABULATE_DATABASE[0]

    # date and warning (verify date)
    date = request.REQUEST.get('request_date')
    warning = None
    try:
        date = str_to_date(date)
    except:
        if date:
            warning = {'text': '日期格式错误'}
        date = datetime.date.today() - datetime.timedelta(days=1)

    # result
    result = _get_monitor_top_karma_consume(db, date, 2)

    ctxt = RequestContext(request, {
        'result': result,
        'warning': warning,
        'date_str': date_to_str(date),
        'selected': {'monitor_top_karma_consume': True},
        'url': reverse('tabulate/monitor_top_karma_consume'),
    })

    return render_to_response('gna/tabulate/monitor_show.html', ctxt)

def _get_monitor_top_karma_consume(db, date, do_type):
    result = {}
    result['title'] = '魂消耗排行榜  ' + _get_date_str(date)
    result['head'] = ['排行', '区服', '角色昵称', '消耗次数', '魂消耗数量']
    result['body'] = []
    
    if date < get_start_date(db):
        return

    objs = get_top_karma_objs_list(db, date, do_type)

    for obj in objs:
        body_row = [{'value':obj.rank_str}, ]
        body_row.append({'value':obj.zone_str})
        body_row.append({'value':obj.user_str})
        body_row.append({'value':obj.times_str})
        body_row.append({'value':obj.amount_str})

        result['body'].append(body_row)

    return result

# 充值用户流失预警排行榜
@login_required
@csrf_protect
def monitor_top_vip7(request):
    db = settings.TABULATE_DATABASE[0]

    # result
    result = _get_monitor_top_vip7(db)

    ctxt = RequestContext(request, {
        'result': result,
        'selected': {'monitor_top_vip7': True},
    })

    return render_to_response('gna/tabulate/monitor_top_vip7.html', ctxt) 

def _get_monitor_top_vip7(db):
    result = {}
    result['title'] = '充值用户流失预警排行榜'
    result['head'] = ['排行', '区服', '角色昵称', '前七天充值金额', '前三天充值金额', '等级', '渠道', '最后更新日期', '用户状态']
    result['body'] = []

    objs = get_top_vip7_objs_list(db)

    for obj in objs:
        body_row = [{'value':obj.rank_str}, ]
        body_row.append({'value':obj.zone_str})
        body_row.append({'value':obj.user_str})
        body_row.append({'value':obj.amount7_str})
        body_row.append({'value':obj.amount3_str})
        body_row.append({'value':obj.lv_str})
        body_row.append({'value':obj.channel_str})
        body_row.append({'value':obj.update_date_str})
        body_row.append({'value':obj.user_type_str})

        result['body'].append(body_row)

    return result

#####
def _filter_objs_value_all_none(objs, filter_values):
    tmp_objs = []
    for obj in objs:
        if not _is_obj_value_all_none(obj, filter_values):
            tmp_objs.append(obj)
    return tmp_objs

def _is_obj_value_all_none(obj, filter_values):
    for value in filter_values:
        if getattr(obj, value) is not None:
            return False
    return True

def _get_date_str(date):
    return date.strftime('%Y/%m/%d')
