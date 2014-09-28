# -*- coding: utf-8 -*-
from django.conf.urls import patterns, include, url

# 首页
urlpatterns = patterns(
    'gna.views.root',
    url(r'^index/$', 'index', name='gna/index'),
)

# gna
urlpatterns += patterns(
    'gna.views.gna_v',
    url(r'^list/$', 'gna_list', name='gna/list'),
    url(r'^detail/daily/(?P<db>\w+)/$', 'gna_daily_detail', name='gna/daily/detail'),
    url(r'^detail/month/(?P<db>\w+)/$', 'gna_month_detail', name='gna/month/detail'),
    url(r'^detail/daily/(?P<db>\w+)/page/(?P<page>\d+)/$', 'gna_daily_detail', name='gna/daily/detail/page'),
    url(r'^detail/month/(?P<db>\w+)/page/(?P<page>\d+)/$', 'gna_month_detail', name='gna/month/detail/page'),

    url(r'^retention/list/$', 'gna_retention_list', name='gna/retention/list'),
    url(r'^retention/detail/daily/(?P<db>\w+)/$', 'gna_retention_daily_detail', name='gna/retention/daily/detail'),
    url(r'^retention/detail/daily/(?P<db>\w+)/page/(?P<page>\d+)/$', 'gna_retention_daily_detail', name='gna/retention/daily/detail/page'),
)

# 日报数据
urlpatterns += patterns(
    'gna.views.tabulate_v',
    url(r'^tabulate/home/$', 'tabulate_home', name='tabulate/home'),

    url(r'^tabulate/daily_date/$', 'daily_date', name='tabulate/daily_date'),
    url(r'^tabulate/daily_date_platform/$', 'daily_date_platform', name='tabulate/daily_date_platform'),
    url(r'^tabulate/daily_platform_date/$', 'daily_platform_date', name='tabulate/daily_platform_date'),
    url(r'^tabulate/daily_date_channel/$', 'daily_date_channel', name='tabulate/daily_date_channel'),
    url(r'^tabulate/daily_channel_date/$', 'daily_channel_date', name='tabulate/daily_channel_date'),
    
    url(r'^tabulate/daily_date/page/(?P<page>\d+)/$', 'daily_date', name='tabulate/daily_date/page'),
    url(r'^tabulate/daily_platform_date/platform/(?P<platform>\d+)/$', 'daily_platform_date', name='tabulate/daily_platform_date/platform'),
    url(r'^tabulate/daily_platform_date/platform/(?P<platform>\d+)/page/(?P<page>\d+)/$', 'daily_platform_date', name='tabulate/daily_platform_date/page'),
    url(r'^tabulate/daily_channel_date/channel/(?P<channel>\d+)/$', 'daily_channel_date', name='tabulate/daily_channel_date/channel'),
    url(r'^tabulate/daily_channel_date/channel/(?P<channel>\d+)/page/(?P<page>\d+)/$', 'daily_channel_date', name='tabulate/daily_channel_date/page'),
)

# 行为数据
urlpatterns += patterns(
    'gna.views.tabulate_behave_v',
    url(r'^tabulate/behave_new_user_level/$', 'behave_new_user_level', name='tabulate/behave_new_user_level'),
    url(r'^tabulate/behave_payment_level/$', 'behave_payment_level', name='tabulate/behave_payment_level'),
    url(r'^tabulate/behave_zel_inc/$', 'behave_zel_inc', name='tabulate/behave_zel_inc'),
    url(r'^tabulate/behave_zel_dec/$', 'behave_zel_dec', name='tabulate/behave_zel_dec'),
    url(r'^tabulate/behave_dia_inc/$', 'behave_dia_inc', name='tabulate/behave_dia_inc'),
    url(r'^tabulate/behave_dia_dec/$', 'behave_dia_dec', name='tabulate/behave_dia_dec'),
    url(r'^tabulate/behave_karma_inc/$', 'behave_karma_inc', name='tabulate/behave_karma_inc'),
    url(r'^tabulate/behave_karma_dec/$', 'behave_karma_dec', name='tabulate/behave_karma_dec'),
    url(r'^tabulate/behave_unit_evo/$', 'behave_unit_evo', name='tabulate/behave_unit_evo'),
    url(r'^tabulate/behave_unit_mix/$', 'behave_unit_mix', name='tabulate/behave_unit_mix'),
    url(r'^tabulate/behave_unit_sell/$', 'behave_unit_sell', name='tabulate/behave_unit_sell'),
    url(r'^tabulate/behave_facility_lvup$', 'behave_facility_lvup', name='tabulate/behave_facility_lvup'),
    url(r'^tabulate/behave_location_lvup$', 'behave_location_lvup', name='tabulate/behave_location_lvup'),
    url(r'^tabulate/behave_arena_challenge$', 'behave_arena_challenge', name='tabulate/behave_arena_challenge'),
    url(r'^tabulate/behave_dungeon_sliver_key$', 'behave_dungeon_sliver_key', name='tabulate/behave_dungeon_sliver_key'),
    url(r'^tabulate/behave_dungeon_gold_key$', 'behave_dungeon_gold_key', name='tabulate/behave_dungeon_gold_key'),
    url(r'^tabulate/behave_bm_refresh$', 'behave_bm_refresh', name='tabulate/behave_bm_refresh'),
    url(r'^tabulate/behave_bm_buy$', 'behave_bm_buy', name='tabulate/behave_bm_buy'),
    url(r'^tabulate/behave_bm_goods$', 'behave_bm_goods', name='tabulate/behave_bm_goods'),
)

# 监控数据
urlpatterns += patterns(
    'gna.views.tabulate_monitor_v',
    url(r'^tabulate/monitor_top_vip/$', 'monitor_top_vip', name='tabulate/monitor_top_vip'),
    url(r'^tabulate/monitor_top_dia_product/$', 'monitor_top_dia_product', name='tabulate/monitor_top_dia_product'),
    url(r'^tabulate/monitor_top_dia_consume/$', 'monitor_top_dia_consume', name='tabulate/monitor_top_dia_consume'),
    url(r'^tabulate/monitor_top_zel_product/$', 'monitor_top_zel_product', name='tabulate/monitor_top_zel_product'),
    url(r'^tabulate/monitor_top_zel_consume/$', 'monitor_top_zel_consume', name='tabulate/monitor_top_zel_consume'),
    url(r'^tabulate/monitor_top_karma_product/$', 'monitor_top_karma_product', name='tabulate/monitor_top_karma_product'),
    url(r'^tabulate/monitor_top_karma_consume/$', 'monitor_top_karma_consume', name='tabulate/monitor_top_karma_consume'),
    url(r'^tabulate/monitor_top_vip7/$', 'monitor_top_vip7', name='tabulate/monitor_top_vip7')
)