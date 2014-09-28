# -*- coding: utf-8 -*-

from django.conf import settings

from collections import defaultdict
import datetime

##### datetime date #####
def str_to_date(date_str):
    return datetime.datetime.strptime(date_str, '%Y-%m-%d').date()

def date_to_str(date):
    return date.strftime('%Y-%m-%d')

def str_to_datetime(datetime_str):
    return datetime.datetime.strptime(datetime_str, '%Y-%m-%d %H:%M:%S.%f')

def datetime_to_str(datetime):
    return datetime.strftime('%Y-%m-%d %H:%M:%S.%f')

def date_to_datetime_begin(date):
    return datetime.datetime(date.year, date.month, date.day, 0, 0, 0)

def date_to_datetime_end(date):
    return datetime.datetime(date.year, date.month, date.day, 23, 59, 59, 999999)

def date_to_month_begin(date):
    return datetime.datetime(date.year, date.month, 1, 0 ,0, 0)

def get_start_date(db):
    return str_to_date(settings.GNA_START_DATE[db])

def date_range(from_date, to_date, to_str=False):
    if type(from_date) == datetime.datetime:
        from_date = from_date.date()
    if type(to_date) == datetime.datetime:
        to_date = to_date.date()
    result = []
    for i in range((to_date-from_date).days+1):
        the_date = from_date + datetime.timedelta(days=i)
        result.append(str(the_date) if to_str else the_date)
    return result

def date_range_since_up(db):
    from_date = get_start_date(db)
    return date_range(from_date, datetime.date.today())

def get_pre_month(dt):
    if dt.month == 1:
        return datetime.datetime(dt.year-1, 12, 1)
    else:
        return datetime.datetime(dt.year, dt.month-1, 1)

def get_next_month(dt):
    if dt.month == 12:
        return datetime.datetime(dt.year+1, 1, 1)
    else:
        return datetime.datetime(dt.year, dt.month+1, 1)

def get_delta_months(dt, months):# 支持负数
    months = int(months)
    dt_year, dt_month = dt.year, dt.month-1
    
    dt_year = dt_year + months/12 + (dt_month + months%12)/12
    dt_month = (dt_month + months%12) % 12
    return datetime.datetime(dt_year, dt_month+1, 1)

def get_delta_months_value(dt1, dt2):
    return (dt1.year-dt2.year)*12 + dt1.month-dt2.month

##### operation ######
def div_operation(a, b):
    return a*1.0/b if b else 0

##### cache key #####
def get_month_cache_key(job_name, datetime):
    month_str = datetime.strftime('%Y%m')
    return job_name + ':' + month_str

def get_retention_cache_key(job_name, retention_days):
    return job_name + ':' + str(retention_days)

def parse_retention_cache_key(retention_cache_key):
    return retention_cache_key.split(':')

##### paginator #####
def paginator(page, cur_page):
    head_limit = settings.GNA_WEB_PAGINATOR_HEAD_LIMIT
    tail_limit = settings.GNA_WEB_PAGINATOR_TAIL_LIMIT
    mid_limit = settings.GNA_WEB_PAGINATOR_MID_LIMIT

    first_block = cur_page-mid_limit > 1+head_limit
    second_block = cur_page+mid_limit < page-tail_limit

    head_page = []
    mid_page = []
    tail_page = []

    if not first_block and not second_block:
        head_page = range(1, page+1)
    elif not first_block and second_block:
        head_page = range(1, cur_page+mid_limit+1)
        mid_page = range(page-tail_limit+1, page+1)
    elif first_block and not second_block:
        head_page = range(1, head_limit+1)
        mid_page = range(cur_page-mid_limit, page+1)
    elif first_block and second_block:
        head_page = range(1, head_limit+1)
        mid_page = range(cur_page-mid_limit, cur_page+mid_limit+1)
        tail_page = range(page-tail_limit, page+1)

    pager = {}
    pager['head_page'] = head_page
    pager['mid_page'] = mid_page
    pager['tail_page'] = tail_page
    pager['cur_page'] = cur_page
    return pager

##### topo_sort #####
def topo_sort(vertexes, edges):
    g = defaultdict(list)
    in_degree = defaultdict(int) 

    for v in vertexes:
        in_degree[v] = 0

    for e in edges:
        u, v = e
        in_degree[v] += 1
        g[u].append(v)

    no_incoming_list = []
    for key, value in in_degree.items():
        if value is 0:
            no_incoming_list.append(key)

    for u in no_incoming_list:
        for v in g[u]:
            in_degree[v] -= 1
            if in_degree[v] is 0:
                no_incoming_list.append(v)

    return no_incoming_list


