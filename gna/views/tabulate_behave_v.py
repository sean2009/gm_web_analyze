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
from gna.tabulate.behave_api import (
    get_new_user_level_objs_list,
    get_new_user_level_summary_objs_list,
    get_payment_level_objs_list,
    get_payment_level_summary_objs_list,
    get_zel_inc_objs_list,
    get_zel_inc_summary_objs_list,
    get_zel_dec_objs_list,
    get_zel_dec_summary_objs_list,
    get_dia_inc_objs_list,
    get_dia_inc_summary_objs_list,
    get_dia_dec_objs_list,
    get_dia_dec_summary_objs_list,
    get_karma_inc_objs_list,
    get_karma_inc_summary_objs_list,
    get_karma_dec_objs_list,
    get_karma_dec_summary_objs_list,
    get_unit_evo_objs_list,
    get_unit_evo_summary_objs_list,
    get_unit_mix_objs_list,
    get_unit_mix_summary_objs_list,
    get_unit_sell_objs_list,
    get_unit_sell_summary_objs_list,
    get_facility_lvup_objs_list,
    get_facility_lvup_summary_objs_list,
    get_location_lvup_objs_list,
    get_location_lvup_summary_objs_list,
    get_arena_challenge_objs_list,
    get_arena_challenge_summary_objs_list,
    get_dungeon_sliver_key_objs_list,
    get_dungeon_sliver_key_summary_objs_list,
    get_dungeon_gold_key_objs_list,
    get_dungeon_gold_key_summary_objs_list,
    get_bm_refresh_objs_list,
    get_bm_refresh_summary_objs_list,
    get_bm_buy_objs_list,
    get_bm_buy_summary_objs_list,
    get_bm_goods_objs_list,
    get_bm_goods_summary_objs_list,
)

# 当日创角等级分布
@login_required
@csrf_protect
def behave_new_user_level(request):
    db = settings.TABULATE_DATABASE[0]
    zone_list = settings.TABULATE_ZONE_LIST

    # date and warning (verify date)
    date = request.REQUEST.get('request_date')
    warning = None
    try:
        date = str_to_date(date)        
    except:
        if date:
            warning = {'text': '日期格式错误'}
        date = datetime.date.today() - datetime.timedelta(days=1)
    
    # zone selected
    try:
        zone_selected = request.REQUEST.get('zone_selected')
        if zone_selected not in zone_list:
            zone_selected = zone_list[0]
    except:
        zone_selected = zone_list[0]
    
    # choices
    choices = []
    for zone in zone_list:
        choices.append({'id': zone, 'name': settings.TABULATE_ZONE_NAME[zone], 'selected': True if zone==zone_selected else False})

    # result
    result = _get_behave_new_user_level_list(db, date, zone_selected)

    ctxt = RequestContext(request, {
        'result': result,
        'warning': warning,
        'date_str': date_to_str(date),
        'selected': {'behave_new_user_level': True},
        'choices': choices,
        'url': reverse('tabulate/behave_new_user_level'),
    })
    return render_to_response('gna/tabulate/behave_show.html', ctxt)

def _get_behave_new_user_level_list(db, date, zone):
    result = {}
    result['title'] = '当日创角等级分布  ' + _get_date_str(date)
    result['head'] = ['区服', '等级', '角色数', '占比', '累计占比']
    result['body'] = []
    
    if date < get_start_date(db):
        return

    if zone == settings.TABULATE_ZONE_LIST[0]:
        objs = get_new_user_level_summary_objs_list(db, date)
    else:
        objs = get_new_user_level_objs_list(db, date, zone)

    objs = _filter_objs_value_all_none(objs, ['lv', 'count', 'percent', 'total_percent'])

    for obj in objs:
        body_row = [{'value':obj.zone_str}, ]
        body_row.append({'value':obj.lv_str})
        body_row.append({'value':obj.count_str})
        body_row.append({'value':obj.percent_str})
        body_row.append({'value':obj.total_percent_str})

        result['body'].append(body_row)

    return result

# 充值档次
@login_required
@csrf_protect
def behave_payment_level(request):
    db = settings.TABULATE_DATABASE[0]
    zone_list = settings.TABULATE_ZONE_LIST

    # date and warning (verify date)
    date = request.REQUEST.get('request_date')
    warning = None
    try:
        date = str_to_date(date)        
    except:
        if date:
            warning = {'text': '日期格式错误'}
        date = datetime.date.today() - datetime.timedelta(days=1)
    
    # zone selected
    try:
        zone_selected = request.REQUEST.get('zone_selected')
        if zone_selected not in zone_list:
            zone_selected = zone_list[0]
    except:
        zone_selected = zone_list[0]
    
    # choices
    choices = []
    for zone in zone_list:
        choices.append({'id': zone, 'name': settings.TABULATE_ZONE_NAME[zone], 'selected': True if zone==zone_selected else False})

    # result
    result = _get_behave_payment_level_list(db, date, zone_selected)

    ctxt = RequestContext(request, {
        'result': result,
        'warning': warning,
        'date_str': date_to_str(date),
        'selected': {'behave_payment_level': True},
        'choices': choices,
        'url': reverse('tabulate/behave_payment_level'),
    })
    return render_to_response('gna/tabulate/behave_show.html', ctxt)

def _get_behave_payment_level_list(db, date, zone):
    result = {}
    result['title'] = '充值档次  ' + _get_date_str(date)
    result['head'] = ['区服', '产品', '角色数', '次数', '总金额']
    result['body'] = []
    
    if date < get_start_date(db):
        return

    if zone == settings.TABULATE_ZONE_LIST[0]:
        objs = get_payment_level_summary_objs_list(db, date)
    else:
        objs = get_payment_level_objs_list(db, date, zone)

    objs = _filter_objs_value_all_none(objs, ['purchase_id', 'user_count', 'times_count', 'amount'])

    for obj in objs:
        body_row = [{'value':obj.zone_str}, ]
        body_row.append({'value':obj.purchase_id_str})
        body_row.append({'value':obj.user_count_str})
        body_row.append({'value':obj.times_count_str})
        body_row.append({'value':obj.amount_str})

        result['body'].append(body_row)

    return result

# 金币产出
@login_required
@csrf_protect
def behave_zel_inc(request):
    db = settings.TABULATE_DATABASE[0]
    zone_list = settings.TABULATE_ZONE_LIST

    # date and warning (verify date)
    date = request.REQUEST.get('request_date')
    warning = None
    try:
        date = str_to_date(date)        
    except:
        if date:
            warning = {'text': '日期格式错误'}
        date = datetime.date.today() - datetime.timedelta(days=1)
    
    # zone selected
    try:
        zone_selected = request.REQUEST.get('zone_selected')
        if zone_selected not in zone_list:
            zone_selected = zone_list[0]
    except:
        zone_selected = zone_list[0]
    
    # choices
    choices = []
    for zone in zone_list:
        choices.append({'id': zone, 'name': settings.TABULATE_ZONE_NAME[zone], 'selected': True if zone==zone_selected else False})

    # result
    result = _get_behave_zel_inc_list(db, date, zone_selected)

    ctxt = RequestContext(request, {
        'result': result,
        'warning': warning,
        'date_str': date_to_str(date),
        'selected': {'behave_zel_inc': True},
        'choices': choices,
        'url': reverse('tabulate/behave_zel_inc'),
    })
    return render_to_response('gna/tabulate/behave_show.html', ctxt)

def _get_behave_zel_inc_list(db, date, zone):
    result = {}
    result['title'] = '金币产出  ' + _get_date_str(date)
    result['head'] = ['区服', '产出渠道', '角色数', '次数', '数量']
    result['body'] = []
    
    if date < get_start_date(db):
        return

    if zone == settings.TABULATE_ZONE_LIST[0]:
        objs = get_zel_inc_summary_objs_list(db, date)
    else:
        objs = get_zel_inc_objs_list(db, date, zone)

    objs = _filter_objs_value_all_none(objs, ['channel_id', 'user_count', 'times_count', 'amount'])

    for obj in objs:
        body_row = [{'value':obj.zone_str}, ]
        body_row.append({'value':obj.channel_id_str})
        body_row.append({'value':obj.user_count_str})
        body_row.append({'value':obj.times_count_str})
        body_row.append({'value':obj.amount_str})

        result['body'].append(body_row)

    return result

# 金币消耗
@login_required
@csrf_protect
def behave_zel_dec(request):
    db = settings.TABULATE_DATABASE[0]
    zone_list = settings.TABULATE_ZONE_LIST

    # date and warning (verify date)
    date = request.REQUEST.get('request_date')
    warning = None
    try:
        date = str_to_date(date)        
    except:
        if date:
            warning = {'text': '日期格式错误'}
        date = datetime.date.today() - datetime.timedelta(days=1)
    
    # zone selected
    try:
        zone_selected = request.REQUEST.get('zone_selected')
        if zone_selected not in zone_list:
            zone_selected = zone_list[0]
    except:
        zone_selected = zone_list[0]
    
    # choices
    choices = []
    for zone in zone_list:
        choices.append({'id': zone, 'name': settings.TABULATE_ZONE_NAME[zone], 'selected': True if zone==zone_selected else False})

    # result
    result = _get_behave_zel_dec_list(db, date, zone_selected)

    ctxt = RequestContext(request, {
        'result': result,
        'warning': warning,
        'date_str': date_to_str(date),
        'selected': {'behave_zel_dec': True},
        'choices': choices,
        'url': reverse('tabulate/behave_zel_dec'),
    })
    return render_to_response('gna/tabulate/behave_show.html', ctxt)

def _get_behave_zel_dec_list(db, date, zone):
    result = {}
    result['title'] = '金币消耗  ' + _get_date_str(date)
    result['head'] = ['区服', '产出渠道', '角色数', '次数', '数量']
    result['body'] = []
    
    if date < get_start_date(db):
        return

    if zone == settings.TABULATE_ZONE_LIST[0]:
        objs = get_zel_dec_summary_objs_list(db, date)
    else:
        objs = get_zel_dec_objs_list(db, date, zone)

    objs = _filter_objs_value_all_none(objs, ['channel_id', 'user_count', 'times_count', 'amount'])

    for obj in objs:
        body_row = [{'value':obj.zone_str}, ]
        body_row.append({'value':obj.channel_id_str})
        body_row.append({'value':obj.user_count_str})
        body_row.append({'value':obj.times_count_str})
        body_row.append({'value':obj.amount_str})

        result['body'].append(body_row)

    return result

# 钻石产出
@login_required
@csrf_protect
def behave_dia_inc(request):
    db = settings.TABULATE_DATABASE[0]
    zone_list = settings.TABULATE_ZONE_LIST

    # date and warning (verify date)
    date = request.REQUEST.get('request_date')
    warning = None
    try:
        date = str_to_date(date)        
    except:
        if date:
            warning = {'text': '日期格式错误'}
        date = datetime.date.today() - datetime.timedelta(days=1)
    
    # zone selected
    try:
        zone_selected = request.REQUEST.get('zone_selected')
        if zone_selected not in zone_list:
            zone_selected = zone_list[0]
    except:
        zone_selected = zone_list[0]
    
    # choices
    choices = []
    for zone in zone_list:
        choices.append({'id': zone, 'name': settings.TABULATE_ZONE_NAME[zone], 'selected': True if zone==zone_selected else False})

    # result
    result = _get_behave_dia_inc_list(db, date, zone_selected)

    ctxt = RequestContext(request, {
        'result': result,
        'warning': warning,
        'date_str': date_to_str(date),
        'selected': {'behave_dia_inc': True},
        'choices': choices,
        'url': reverse('tabulate/behave_dia_inc'),
    })
    return render_to_response('gna/tabulate/behave_show.html', ctxt)

def _get_behave_dia_inc_list(db, date, zone):
    result = {}
    result['title'] = '钻石产出  ' + _get_date_str(date)
    result['head'] = ['区服', '产出渠道', '角色数', '次数', '数量']
    result['body'] = []
    
    if date < get_start_date(db):
        return

    if zone == settings.TABULATE_ZONE_LIST[0]:
        objs = get_dia_inc_summary_objs_list(db, date)
    else:
        objs = get_dia_inc_objs_list(db, date, zone)

    objs = _filter_objs_value_all_none(objs, ['channel_id', 'user_count', 'times_count', 'amount'])

    for obj in objs:
        body_row = [{'value':obj.zone_str}, ]
        body_row.append({'value':obj.channel_id_str})
        body_row.append({'value':obj.user_count_str})
        body_row.append({'value':obj.times_count_str})
        body_row.append({'value':obj.amount_str})

        result['body'].append(body_row)

    return result

# 钻石消耗
@login_required
@csrf_protect
def behave_dia_dec(request):
    db = settings.TABULATE_DATABASE[0]
    zone_list = settings.TABULATE_ZONE_LIST

    # date and warning (verify date)
    date = request.REQUEST.get('request_date')
    warning = None
    try:
        date = str_to_date(date)        
    except:
        if date:
            warning = {'text': '日期格式错误'}
        date = datetime.date.today() - datetime.timedelta(days=1)
    
    # zone selected
    try:
        zone_selected = request.REQUEST.get('zone_selected')
        if zone_selected not in zone_list:
            zone_selected = zone_list[0]
    except:
        zone_selected = zone_list[0]
    
    # choices
    choices = []
    for zone in zone_list:
        choices.append({'id': zone, 'name': settings.TABULATE_ZONE_NAME[zone], 'selected': True if zone==zone_selected else False})

    # result
    result = _get_behave_dia_dec_list(db, date, zone_selected)

    ctxt = RequestContext(request, {
        'result': result,
        'warning': warning,
        'date_str': date_to_str(date),
        'selected': {'behave_dia_dec': True},
        'choices': choices,
        'url': reverse('tabulate/behave_dia_dec')
    })
    return render_to_response('gna/tabulate/behave_show.html', ctxt)

def _get_behave_dia_dec_list(db, date, zone):
    result = {}
    result['title'] = '钻石消耗  ' + _get_date_str(date)
    result['head'] = ['区服', '产出渠道', '角色数', '次数', '数量']
    result['body'] = []
    
    if date < get_start_date(db):
        return

    if zone == settings.TABULATE_ZONE_LIST[0]:
        objs = get_dia_dec_summary_objs_list(db, date)
    else:
        objs = get_dia_dec_objs_list(db, date, zone)

    objs = _filter_objs_value_all_none(objs, ['channel_id', 'user_count', 'times_count', 'amount'])

    for obj in objs:
        body_row = [{'value':obj.zone_str}, ]
        body_row.append({'value':obj.channel_id_str})
        body_row.append({'value':obj.user_count_str})
        body_row.append({'value':obj.times_count_str})
        body_row.append({'value':obj.amount_str})

        result['body'].append(body_row)

    return result

# 魂产出
@login_required
@csrf_protect
def behave_karma_inc(request):
    db = settings.TABULATE_DATABASE[0]
    zone_list = settings.TABULATE_ZONE_LIST

    # date and warning (verify date)
    date = request.REQUEST.get('request_date')
    warning = None
    try:
        date = str_to_date(date)        
    except:
        if date:
            warning = {'text': '日期格式错误'}
        date = datetime.date.today() - datetime.timedelta(days=1)
    
    # zone selected
    try:
        zone_selected = request.REQUEST.get('zone_selected')
        if zone_selected not in zone_list:
            zone_selected = zone_list[0]
    except:
        zone_selected = zone_list[0]
    
    # choices
    choices = []
    for zone in zone_list:
        choices.append({'id': zone, 'name': settings.TABULATE_ZONE_NAME[zone], 'selected': True if zone==zone_selected else False})

    # result
    result = _get_behave_karma_inc_list(db, date, zone_selected)

    ctxt = RequestContext(request, {
        'result': result,
        'warning': warning,
        'date_str': date_to_str(date),
        'selected': {'behave_karma_inc': True},
        'choices': choices,
        'url': reverse('tabulate/behave_karma_inc'),
    })
    return render_to_response('gna/tabulate/behave_show.html', ctxt)

def _get_behave_karma_inc_list(db, date, zone):
    result = {}
    result['title'] = '魂产出  ' + _get_date_str(date)
    result['head'] = ['区服', '产出渠道', '角色数', '次数', '数量']
    result['body'] = []
    
    if date < get_start_date(db):
        return

    if zone == settings.TABULATE_ZONE_LIST[0]:
        objs = get_karma_inc_summary_objs_list(db, date)
    else:
        objs = get_karma_inc_objs_list(db, date, zone)

    objs = _filter_objs_value_all_none(objs, ['channel_id', 'user_count', 'times_count', 'amount'])

    for obj in objs:
        body_row = [{'value':obj.zone_str}, ]
        body_row.append({'value':obj.channel_id_str})
        body_row.append({'value':obj.user_count_str})
        body_row.append({'value':obj.times_count_str})
        body_row.append({'value':obj.amount_str})

        result['body'].append(body_row)

    return result

# 魂消耗
@login_required
@csrf_protect
def behave_karma_dec(request):
    db = settings.TABULATE_DATABASE[0]
    zone_list = settings.TABULATE_ZONE_LIST

    # date and warning (verify date)
    date = request.REQUEST.get('request_date')
    warning = None
    try:
        date = str_to_date(date)        
    except:
        if date:
            warning = {'text': '日期格式错误'}
        date = datetime.date.today() - datetime.timedelta(days=1)
    
    # zone selected
    try:
        zone_selected = request.REQUEST.get('zone_selected')
        if zone_selected not in zone_list:
            zone_selected = zone_list[0]
    except:
        zone_selected = zone_list[0]
    
    # choices
    choices = []
    for zone in zone_list:
        choices.append({'id': zone, 'name': settings.TABULATE_ZONE_NAME[zone], 'selected': True if zone==zone_selected else False})

    # result
    result = _get_behave_karma_dec_list(db, date, zone_selected)

    ctxt = RequestContext(request, {
        'result': result,
        'warning': warning,
        'date_str': date_to_str(date),
        'selected': {'behave_karma_dec': True},
        'choices': choices,
        'url': reverse('tabulate/behave_karma_dec'),
    })
    return render_to_response('gna/tabulate/behave_show.html', ctxt)

def _get_behave_karma_dec_list(db, date, zone):
    result = {}
    result['title'] = '魂消耗  ' + _get_date_str(date)
    result['head'] = ['区服', '产出渠道', '角色数', '次数', '数量']
    result['body'] = []
    
    if date < get_start_date(db):
        return

    if zone == settings.TABULATE_ZONE_LIST[0]:
        objs = get_karma_dec_summary_objs_list(db, date)
    else:
        objs = get_karma_dec_objs_list(db, date, zone)

    objs = _filter_objs_value_all_none(objs, ['channel_id', 'user_count', 'times_count', 'amount'])

    for obj in objs:
        body_row = [{'value':obj.zone_str}, ]
        body_row.append({'value':obj.channel_id_str})
        body_row.append({'value':obj.user_count_str})
        body_row.append({'value':obj.times_count_str})
        body_row.append({'value':obj.amount_str})

        result['body'].append(body_row)

    return result

# 卡牌进化
@login_required
@csrf_protect
def behave_unit_evo(request):
    db = settings.TABULATE_DATABASE[0]
    zone_list = settings.TABULATE_ZONE_LIST

    # date and warning (verify date)
    date = request.REQUEST.get('request_date')
    warning = None
    try:
        date = str_to_date(date)        
    except:
        if date:
            warning = {'text': '日期格式错误'}
        date = datetime.date.today() - datetime.timedelta(days=1)
    
    # zone selected
    try:
        zone_selected = request.REQUEST.get('zone_selected')
        if zone_selected not in zone_list:
            zone_selected = zone_list[0]
    except:
        zone_selected = zone_list[0]
    
    # choices
    choices = []
    for zone in zone_list:
        choices.append({'id': zone, 'name': settings.TABULATE_ZONE_NAME[zone], 'selected': True if zone==zone_selected else False})

    # result
    result = _get_behave_unit_evo_list(db, date, zone_selected)

    ctxt = RequestContext(request, {
        'result': result,
        'warning': warning,
        'date_str': date_to_str(date),
        'selected': {'behave_unit_evo': True},
        'choices': choices,
        'url': reverse('tabulate/behave_unit_evo'),
    })
    return render_to_response('gna/tabulate/behave_show.html', ctxt)

def _get_behave_unit_evo_list(db, date, zone):
    result = {}
    result['title'] = '卡牌进化  ' + _get_date_str(date)
    result['head'] = ['区服', '角色数', '次数']
    result['body'] = []
    
    if date < get_start_date(db):
        return

    if zone == settings.TABULATE_ZONE_LIST[0]:
        objs = get_unit_evo_summary_objs_list(db, date)
    else:
        objs = get_unit_evo_objs_list(db, date, zone)

    objs = _filter_objs_value_all_none(objs, ['user_count', 'times_count'])

    for obj in objs:
        body_row = [{'value':obj.zone_str}, ]
        body_row.append({'value':obj.user_count_str})
        body_row.append({'value':obj.times_count_str})

        result['body'].append(body_row)

    return result

# 卡牌强化
@login_required
@csrf_protect
def behave_unit_mix(request):
    db = settings.TABULATE_DATABASE[0]
    zone_list = settings.TABULATE_ZONE_LIST

    # date and warning (verify date)
    date = request.REQUEST.get('request_date')
    warning = None
    try:
        date = str_to_date(date)        
    except:
        if date:
            warning = {'text': '日期格式错误'}
        date = datetime.date.today() - datetime.timedelta(days=1)
    
    # zone selected
    try:
        zone_selected = request.REQUEST.get('zone_selected')
        if zone_selected not in zone_list:
            zone_selected = zone_list[0]
    except:
        zone_selected = zone_list[0]
    
    # choices
    choices = []
    for zone in zone_list:
        choices.append({'id': zone, 'name': settings.TABULATE_ZONE_NAME[zone], 'selected': True if zone==zone_selected else False})

    # result
    result = _get_behave_unit_mix_list(db, date, zone_selected)

    ctxt = RequestContext(request, {
        'result': result,
        'warning': warning,
        'date_str': date_to_str(date),
        'selected': {'behave_unit_mix': True},
        'choices': choices,
        'url': reverse('tabulate/behave_unit_mix'),
    })
    return render_to_response('gna/tabulate/behave_show.html', ctxt)

def _get_behave_unit_mix_list(db, date, zone):
    result = {}
    result['title'] = '卡牌强化  ' + _get_date_str(date)
    result['head'] = ['区服', '角色数', '次数']
    result['body'] = []
    
    if date < get_start_date(db):
        return

    if zone == settings.TABULATE_ZONE_LIST[0]:
        objs = get_unit_mix_summary_objs_list(db, date)
    else:
        objs = get_unit_mix_objs_list(db, date, zone)

    objs = _filter_objs_value_all_none(objs, ['user_count', 'times_count'])

    for obj in objs:
        body_row = [{'value':obj.zone_str}, ]
        body_row.append({'value':obj.user_count_str})
        body_row.append({'value':obj.times_count_str})

        result['body'].append(body_row)

    return result

# 卡牌出售
@login_required
@csrf_protect
def behave_unit_sell(request):
    db = settings.TABULATE_DATABASE[0]
    zone_list = settings.TABULATE_ZONE_LIST

    # date and warning (verify date)
    date = request.REQUEST.get('request_date')
    warning = None
    try:
        date = str_to_date(date)        
    except:
        if date:
            warning = {'text': '日期格式错误'}
        date = datetime.date.today() - datetime.timedelta(days=1)
    
    # zone selected
    try:
        zone_selected = request.REQUEST.get('zone_selected')
        if zone_selected not in zone_list:
            zone_selected = zone_list[0]
    except:
        zone_selected = zone_list[0]
    
    # choices
    choices = []
    for zone in zone_list:
        choices.append({'id': zone, 'name': settings.TABULATE_ZONE_NAME[zone], 'selected': True if zone==zone_selected else False})

    # result
    result = _get_behave_unit_sell_list(db, date, zone_selected)

    ctxt = RequestContext(request, {
        'result': result,
        'warning': warning,
        'date_str': date_to_str(date),
        'selected': {'behave_unit_sell': True},
        'choices': choices,
        'url': reverse('tabulate/behave_unit_sell'),
    })
    return render_to_response('gna/tabulate/behave_show.html', ctxt)

def _get_behave_unit_sell_list(db, date, zone):
    result = {}
    result['title'] = '卡牌出售  ' + _get_date_str(date)
    result['head'] = ['区服', '角色数', '次数']
    result['body'] = []
    
    if date < get_start_date(db):
        return

    if zone == settings.TABULATE_ZONE_LIST[0]:
        objs = get_unit_sell_summary_objs_list(db, date)
    else:
        objs = get_unit_sell_objs_list(db, date, zone)

    objs = _filter_objs_value_all_none(objs, ['user_count', 'times_count'])

    for obj in objs:
        body_row = [{'value':obj.zone_str}, ]
        body_row.append({'value':obj.user_count_str})
        body_row.append({'value':obj.times_count_str})

        result['body'].append(body_row)

    return result

# 建筑升级
@login_required
@csrf_protect
def behave_facility_lvup(request):
    db = settings.TABULATE_DATABASE[0]
    zone_list = settings.TABULATE_ZONE_LIST

    # date and warning (verify date)
    date = request.REQUEST.get('request_date')
    warning = None
    try:
        date = str_to_date(date)        
    except:
        if date:
            warning = {'text': '日期格式错误'}
        date = datetime.date.today() - datetime.timedelta(days=1)
    
    # zone selected
    try:
        zone_selected = request.REQUEST.get('zone_selected')
        if zone_selected not in zone_list:
            zone_selected = zone_list[0]
    except:
        zone_selected = zone_list[0]
    
    # choices
    choices = []
    for zone in zone_list:
        choices.append({'id': zone, 'name': settings.TABULATE_ZONE_NAME[zone], 'selected': True if zone==zone_selected else False})

    # result
    result = _get_behave_facility_lvup_list(db, date, zone_selected)

    ctxt = RequestContext(request, {
        'result': result,
        'warning': warning,
        'date_str': date_to_str(date),
        'selected': {'behave_facility_lvup': True},
        'choices': choices,
        'url': reverse('tabulate/behave_facility_lvup'),
    })
    return render_to_response('gna/tabulate/behave_show.html', ctxt)

def _get_behave_facility_lvup_list(db, date, zone):
    result = {}
    result['title'] = '建筑升级  ' + _get_date_str(date)
    result['head'] = ['区服', '建筑位置', '角色数', '次数']
    result['body'] = []
    
    if date < get_start_date(db):
        return

    if zone == settings.TABULATE_ZONE_LIST[0]:
        objs = get_facility_lvup_summary_objs_list(db, date)
    else:
        objs = get_facility_lvup_objs_list(db, date, zone)

    objs = _filter_objs_value_all_none(objs, ['user_count', 'times_count'])

    for obj in objs:
        body_row = [{'value':obj.zone_str}, ]
        body_row.append({'value':obj.facility_id_str})
        body_row.append({'value':obj.user_count_str})
        body_row.append({'value':obj.times_count_str})

        result['body'].append(body_row)

    return result

# 资源升级
@login_required
@csrf_protect
def behave_location_lvup(request):
    db = settings.TABULATE_DATABASE[0]
    zone_list = settings.TABULATE_ZONE_LIST

    # date and warning (verify date)
    date = request.REQUEST.get('request_date')
    warning = None
    try:
        date = str_to_date(date)        
    except:
        if date:
            warning = {'text': '日期格式错误'}
        date = datetime.date.today() - datetime.timedelta(days=1)
    
    # zone selected
    try:
        zone_selected = request.REQUEST.get('zone_selected')
        if zone_selected not in zone_list:
            zone_selected = zone_list[0]
    except:
        zone_selected = zone_list[0]
    
    # choices
    choices = []
    for zone in zone_list:
        choices.append({'id': zone, 'name': settings.TABULATE_ZONE_NAME[zone], 'selected': True if zone==zone_selected else False})

    # result
    result = _get_behave_location_lvup_list(db, date, zone_selected)

    ctxt = RequestContext(request, {
        'result': result,
        'warning': warning,
        'date_str': date_to_str(date),
        'selected': {'behave_location_lvup': True},
        'choices': choices,
        'url': reverse('tabulate/behave_location_lvup'),
    })
    return render_to_response('gna/tabulate/behave_show.html', ctxt)

def _get_behave_location_lvup_list(db, date, zone):
    result = {}
    result['title'] = '资源升级  ' + _get_date_str(date)
    result['head'] = ['区服', '资源位置', '角色数', '次数']
    result['body'] = []
    
    if date < get_start_date(db):
        return

    if zone == settings.TABULATE_ZONE_LIST[0]:
        objs = get_location_lvup_summary_objs_list(db, date)
    else:
        objs = get_location_lvup_objs_list(db, date, zone)

    objs = _filter_objs_value_all_none(objs, ['user_count', 'times_count'])

    for obj in objs:
        body_row = [{'value':obj.zone_str}, ]
        body_row.append({'value':obj.location_id_str})
        body_row.append({'value':obj.user_count_str})
        body_row.append({'value':obj.times_count_str})

        result['body'].append(body_row)

    return result

# 竞技场挑战
@login_required
@csrf_protect
def behave_arena_challenge(request):
    db = settings.TABULATE_DATABASE[0]
    zone_list = settings.TABULATE_ZONE_LIST

    # date and warning (verify date)
    date = request.REQUEST.get('request_date')
    warning = None
    try:
        date = str_to_date(date)        
    except:
        if date:
            warning = {'text': '日期格式错误'}
        date = datetime.date.today() - datetime.timedelta(days=1)
    
    # zone selected
    try:
        zone_selected = request.REQUEST.get('zone_selected')
        if zone_selected not in zone_list:
            zone_selected = zone_list[0]
    except:
        zone_selected = zone_list[0]
    
    # choices
    choices = []
    for zone in zone_list:
        choices.append({'id': zone, 'name': settings.TABULATE_ZONE_NAME[zone], 'selected': True if zone==zone_selected else False})

    # result
    result = _get_behave_arena_challenge_list(db, date, zone_selected)

    ctxt = RequestContext(request, {
        'result': result,
        'warning': warning,
        'date_str': date_to_str(date),
        'selected': {'behave_arena_challenge': True},
        'choices': choices,
        'url': reverse('tabulate/behave_arena_challenge'),
    })
    return render_to_response('gna/tabulate/behave_show.html', ctxt)

def _get_behave_arena_challenge_list(db, date, zone):
    result = {}
    result['title'] = '竞技场挑战  ' + _get_date_str(date)
    result['head'] = ['区服', '状态', '角色数', '次数', '积分获得量', '魂产出数量']
    result['body'] = []
    
    if date < get_start_date(db):
        return

    if zone == settings.TABULATE_ZONE_LIST[0]:
        objs = get_arena_challenge_summary_objs_list(db, date)
    else:
        objs = get_arena_challenge_objs_list(db, date, zone)

    objs = _filter_objs_value_all_none(objs, ['user_count', 'times_count'])

    for obj in objs:
        body_row = [{'value':obj.zone_str}, ]
        body_row.append({'value':obj.result_str})
        body_row.append({'value':obj.user_count_str})
        body_row.append({'value':obj.times_count_str})
        body_row.append({'value':obj.point_count_str})
        body_row.append({'value':obj.karma_count_str})

        result['body'].append(body_row)

    return result

# 帝都兰德尔-银钥匙
@login_required
@csrf_protect
def behave_dungeon_sliver_key(request):
    db = settings.TABULATE_DATABASE[0]
    zone_list = settings.TABULATE_ZONE_LIST

    # date and warning (verify date)
    date = request.REQUEST.get('request_date')
    warning = None
    try:
        date = str_to_date(date)        
    except:
        if date:
            warning = {'text': '日期格式错误'}
        date = datetime.date.today() - datetime.timedelta(days=1)
    
    # zone selected
    try:
        zone_selected = request.REQUEST.get('zone_selected')
        if zone_selected not in zone_list:
            zone_selected = zone_list[0]
    except:
        zone_selected = zone_list[0]
    
    # choices
    choices = []
    for zone in zone_list:
        choices.append({'id': zone, 'name': settings.TABULATE_ZONE_NAME[zone], 'selected': True if zone==zone_selected else False})

    # result
    result = _get_behave_dungeon_sliver_key_list(db, date, zone_selected)

    ctxt = RequestContext(request, {
        'result': result,
        'warning': warning,
        'date_str': date_to_str(date),
        'selected': {'behave_dungeon_sliver_key': True},
        'choices': choices,
        'url': reverse('tabulate/behave_dungeon_sliver_key'),
    })
    return render_to_response('gna/tabulate/behave_show.html', ctxt)

def _get_behave_dungeon_sliver_key_list(db, date, zone):
    result = {}
    result['title'] = '帝都兰德尔-银钥匙  ' + _get_date_str(date)
    result['head'] = ['区服', '状态', '角色数', '次数', '钥匙数']
    result['body'] = []
    
    if date < get_start_date(db):
        return

    if zone == settings.TABULATE_ZONE_LIST[0]:
        objs = get_dungeon_sliver_key_summary_objs_list(db, date)
    else:
        objs = get_dungeon_sliver_key_objs_list(db, date, zone)

    objs = _filter_objs_value_all_none(objs, ['user_count', 'times_count'])

    for obj in objs:
        body_row = [{'value':obj.zone_str}, ]
        body_row.append({'value':obj.do_type_str})
        body_row.append({'value':obj.user_count_str})
        body_row.append({'value':obj.times_count_str})
        body_row.append({'value':obj.key_count_str})

        result['body'].append(body_row)

    return result

# 帝都兰德尔-金钥匙
@login_required
@csrf_protect
def behave_dungeon_gold_key(request):
    db = settings.TABULATE_DATABASE[0]
    zone_list = settings.TABULATE_ZONE_LIST

    # date and warning (verify date)
    date = request.REQUEST.get('request_date')
    warning = None
    try:
        date = str_to_date(date)        
    except:
        if date:
            warning = {'text': '日期格式错误'}
        date = datetime.date.today() - datetime.timedelta(days=1)
    
    # zone selected
    try:
        zone_selected = request.REQUEST.get('zone_selected')
        if zone_selected not in zone_list:
            zone_selected = zone_list[0]
    except:
        zone_selected = zone_list[0]
    
    # choices
    choices = []
    for zone in zone_list:
        choices.append({'id': zone, 'name': settings.TABULATE_ZONE_NAME[zone], 'selected': True if zone==zone_selected else False})

    # result
    result = _get_behave_dungeon_gold_key_list(db, date, zone_selected)

    ctxt = RequestContext(request, {
        'result': result,
        'warning': warning,
        'date_str': date_to_str(date),
        'selected': {'behave_dungeon_gold_key': True},
        'choices': choices,
        'url': reverse('tabulate/behave_dungeon_gold_key'),
    })
    return render_to_response('gna/tabulate/behave_show.html', ctxt)

def _get_behave_dungeon_gold_key_list(db, date, zone):
    result = {}
    result['title'] = '帝都兰德尔-金钥匙  ' + _get_date_str(date)
    result['head'] = ['区服', '状态', '角色数', '次数', '钥匙数']
    result['body'] = []
    
    if date < get_start_date(db):
        return

    if zone == settings.TABULATE_ZONE_LIST[0]:
        objs = get_dungeon_gold_key_summary_objs_list(db, date)
    else:
        objs = get_dungeon_gold_key_objs_list(db, date, zone)

    objs = _filter_objs_value_all_none(objs, ['user_count', 'times_count'])

    for obj in objs:
        body_row = [{'value':obj.zone_str}, ]
        body_row.append({'value':obj.do_type_str})
        body_row.append({'value':obj.user_count_str})
        body_row.append({'value':obj.times_count_str})
        body_row.append({'value':obj.key_count_str})

        result['body'].append(body_row)

    return result

# 黑市刷新
@login_required
@csrf_protect
def behave_bm_refresh(request):
    db = settings.TABULATE_DATABASE[0]
    zone_list = settings.TABULATE_ZONE_LIST

    # date and warning (verify date)
    date = request.REQUEST.get('request_date')
    warning = None
    try:
        date = str_to_date(date)        
    except:
        if date:
            warning = {'text': '日期格式错误'}
        date = datetime.date.today() - datetime.timedelta(days=1)
    
    # zone selected
    try:
        zone_selected = request.REQUEST.get('zone_selected')
        if zone_selected not in zone_list:
            zone_selected = zone_list[0]
    except:
        zone_selected = zone_list[0]
    
    # choices
    choices = []
    for zone in zone_list:
        choices.append({'id': zone, 'name': settings.TABULATE_ZONE_NAME[zone], 'selected': True if zone==zone_selected else False})

    # result
    result = _get_behave_bm_refresh_list(db, date, zone_selected)

    ctxt = RequestContext(request, {
        'result': result,
        'warning': warning,
        'date_str': date_to_str(date),
        'selected': {'behave_bm_refresh': True},
        'choices': choices,
        'url': reverse('tabulate/behave_bm_refresh'),
    })
    return render_to_response('gna/tabulate/behave_show.html', ctxt)

def _get_behave_bm_refresh_list(db, date, zone):
    result = {}
    result['title'] = '黑市刷新  ' + _get_date_str(date)
    result['head'] = ['区服', '货币类型', '角色数', '次数', '货币数量']
    result['body'] = []
    
    if date < get_start_date(db):
        return

    if zone == settings.TABULATE_ZONE_LIST[0]:
        objs = get_bm_refresh_summary_objs_list(db, date)
    else:
        objs = get_bm_refresh_objs_list(db, date, zone)

    objs = _filter_objs_value_all_none(objs, ['user_count', 'times_count'])

    for obj in objs:
        body_row = [{'value':obj.zone_str}, ]
        body_row.append({'value':obj.money_type_str})
        body_row.append({'value':obj.user_count_str})
        body_row.append({'value':obj.times_count_str})
        body_row.append({'value':obj.amount_str})

        result['body'].append(body_row)

    return result

# 黑市购买
@login_required
@csrf_protect
def behave_bm_buy(request):
    db = settings.TABULATE_DATABASE[0]
    zone_list = settings.TABULATE_ZONE_LIST

    # date and warning (verify date)
    date = request.REQUEST.get('request_date')
    warning = None
    try:
        date = str_to_date(date)        
    except:
        if date:
            warning = {'text': '日期格式错误'}
        date = datetime.date.today() - datetime.timedelta(days=1)
    
    # zone selected
    try:
        zone_selected = request.REQUEST.get('zone_selected')
        if zone_selected not in zone_list:
            zone_selected = zone_list[0]
    except:
        zone_selected = zone_list[0]
    
    # choices
    choices = []
    for zone in zone_list:
        choices.append({'id': zone, 'name': settings.TABULATE_ZONE_NAME[zone], 'selected': True if zone==zone_selected else False})

    # result
    result = _get_behave_bm_buy_list(db, date, zone_selected)

    ctxt = RequestContext(request, {
        'result': result,
        'warning': warning,
        'date_str': date_to_str(date),
        'selected': {'behave_bm_buy': True},
        'choices': choices,
        'url': reverse('tabulate/behave_bm_buy'),
    })
    return render_to_response('gna/tabulate/behave_show.html', ctxt)

def _get_behave_bm_buy_list(db, date, zone):
    result = {}
    result['title'] = '黑市购买  ' + _get_date_str(date)
    result['head'] = ['区服', '货币类型', '角色数', '次数', '货币数量']
    result['body'] = []
    
    if date < get_start_date(db):
        return

    if zone == settings.TABULATE_ZONE_LIST[0]:
        objs = get_bm_buy_summary_objs_list(db, date)
    else:
        objs = get_bm_buy_objs_list(db, date, zone)

    objs = _filter_objs_value_all_none(objs, ['user_count', 'times_count'])

    for obj in objs:
        body_row = [{'value':obj.zone_str}, ]
        body_row.append({'value':obj.money_type_str})
        body_row.append({'value':obj.user_count_str})
        body_row.append({'value':obj.times_count_str})
        body_row.append({'value':obj.amount_str})

        result['body'].append(body_row)

    return result

# 黑市物品购买情况
@login_required
@csrf_protect
def behave_bm_goods(request):
    db = settings.TABULATE_DATABASE[0]
    zone_list = settings.TABULATE_ZONE_LIST

    # date and warning (verify date)
    date = request.REQUEST.get('request_date')
    warning = None
    try:
        date = str_to_date(date)        
    except:
        if date:
            warning = {'text': '日期格式错误'}
        date = datetime.date.today() - datetime.timedelta(days=1)
    
    # zone selected
    try:
        zone_selected = request.REQUEST.get('zone_selected')
        if zone_selected not in zone_list:
            zone_selected = zone_list[0]
    except:
        zone_selected = zone_list[0]
    
    # choices
    choices = []
    for zone in zone_list:
        choices.append({'id': zone, 'name': settings.TABULATE_ZONE_NAME[zone], 'selected': True if zone==zone_selected else False})

    # result
    result = _get_behave_bm_goods_list(db, date, zone_selected)

    ctxt = RequestContext(request, {
        'result': result,
        'warning': warning,
        'date_str': date_to_str(date),
        'selected': {'behave_bm_goods': True},
        'choices': choices,
        'url': reverse('tabulate/behave_bm_goods'),
    })
    return render_to_response('gna/tabulate/behave_show.html', ctxt)

def _get_behave_bm_goods_list(db, date, zone):
    result = {}
    result['title'] = '黑市物品购买情况  ' + _get_date_str(date)
    result['head'] = ['区服', '物品', '角色数', '次数']
    result['body'] = []
    
    if date < get_start_date(db):
        return

    if zone == settings.TABULATE_ZONE_LIST[0]:
        objs = get_bm_goods_summary_objs_list(db, date)
    else:
        objs = get_bm_goods_objs_list(db, date, zone)

    objs = _filter_objs_value_all_none(objs, ['user_count', 'times_count'])

    for obj in objs:
        body_row = [{'value':obj.zone_str}, ]
        body_row.append({'value':obj.goods_str})
        body_row.append({'value':obj.user_count_str})
        body_row.append({'value':obj.times_count_str})

        result['body'].append(body_row)

    return result

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
