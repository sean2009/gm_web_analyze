# -*- coding: utf-8 -*-
import os
from settings.base import *

GNA_RETENTION_DAYS_LIST = [1,2,3,4,5,6,7,14,30,60,90]

# web settings
GNA_WEB_LIST_DAILY_LIMIT = 5
GNA_WEB_LIST_MONTH_LIMIT = 1
GNA_WEB_DETAIL_DAILY_LIMIT = 10
GNA_WEB_DETAIL_MONTH_LIMIT = 12

GNA_WEB_PAGINATOR_HEAD_LIMIT = 1
GNA_WEB_PAGINATOR_TAIL_LIMIT = 1
GNA_WEB_PAGINATOR_MID_LIMIT = 1

##### tabulate settings #####

# tabulate daily
TABULATE_WEB_LIST_DAILY_DATE_LIMIT = 30
TABULATE_WEB_LIST_DAILY_DATE_PLATFORM_LIMIT = 1000
TABULATE_WEB_LIST_DAILY_PLATFORM_DATE_LIMIT = 30
TABULATE_WEB_LIST_DAILY_DATE_CHANNEL_LIMIT = 1000
TABULATE_WEB_LIST_DAILY_CHANNEL_DATE_LIMIT = 30

TABULATE_FILTER_LC1_RATIO_GT = 0.38
TABULATE_FILTER_LC2_RATIO_GT = 1
TABULATE_FILTER_LC3_RATIO_GT = 0.26
TABULATE_FILTER_LC4_RATIO_GT = 1
TABULATE_FILTER_LC5_RATIO_GT = 1
TABULATE_FILTER_LC6_RATIO_GT = 1
TABULATE_FILTER_LC7_RATIO_GT = 0.18
TABULATE_FILTER_LC14_RATIO_GT = 0.10
TABULATE_FILTER_LC30_RATIO_GT = 0.05
TABULATE_FILTER_VIP_RATIO_GT = 0.028
TABULATE_FILTER_ARPPU_GT = 120

# tabulate behave
TABULATE_PURCHASE_ID_NAME = {1:'月卡',2:'小堆钻石',3:'小袋钻石',4:'大袋钻石',5:'小箱钻石',6:'大箱钻石',7:'钻石宝库'}
TABULATE_RESOURCE_CHANNEL_ID_NAME = {
    0: '活动赠送的礼品',
    1: '体力',
    2: '伙伴栏',
    3: '仓库栏',
    4: '竞技点',
    5: '前线猎人竞技点',
    6: '购买钻石',
    7: '限时礼包',
    1001: '初始化',
    1002: '用户做成',
    1003: '用户信息获取',
    1005: 'ACTION_TYPE_GET_USER_DATA',
    1006: '最新信息更新',
    1007: '玩家信息获取',
    1008: '新手引导信息更新',
    1009: '脚本信息更新',
    1010: 'ACTION_TYPE_NGWORD_CHECK',
    1011: 'ACTION_TYPE_UPDATE_INFO_LIGHT',
    1012: 'ACTION_TYPE_UPDATE_EVENT_INFO',
    1090: '跳过tuto',
    2004: 'ACTION_TYPE_SETTING_INFO',
    2005: 'ACTION_TYPE_FRIEND_GET',
    2006: '好友删除',
    2008: '好友申请',
    2009: 'ACTION_TYPE_FRIEND_GET_AGREE',
    2010: '好友接受',
    2011: '好友拒绝',
    2013: '好友搜索',
    2016: 'ACTION_TYPE_FRIEND_FAVORITE',
    2030: 'ACTION_TYPE_LITTLE_GUILD_CREATE',
    2031: 'ACTION_TYPE_LITTLE_GUILD_UPDATE',
    2032: 'ACTION_TYPE_LITTLE_GUILD_REQUEST',
    2033: 'ACTION_TYPE_LITTLE_GUILD_INVITE',
    2034: 'ACTION_TYPE_LITTLE_GUILD_AGREE',
    2035: 'ACTION_TYPE_LITTLE_GUILD_REFUSE',
    2036: 'ACTION_TYPE_LITTLE_GUILD_DELETE',
    2037: 'ACTION_TYPE_LITTLE_GUILD_QUIT',
    2038: 'ACTION_TYPE_LITTLE_GUILD_SEARCH',
    2039: 'ACTION_TYPE_LITTLE_GUILD_CANCEL',
    2040: 'ACTION_TYPE_LITTLE_GUILD_AUTO_JOIN',
    2101: '道具编成',
    2102: '合成装备',
    2103: '道具售出',
    2104: '道具装备',
    2201: 'ACTION_TYPE_TOWN_ENTER',
    2202: '村庄产出',
    2203: '村庄建筑升级',
    2301: 'ACTION_TYPE_GET_GIFT_INFO',
    2302: '礼包信息修正',
    2401: '领取邀请特典',
    2501: '接收钥匙',
    2502: '使用钥匙',
    2503: 'ACTION_TYPE_GET_DISTRIBUTE_DUNGEON_KEY_INFO',
    2504: 'ACTION_TYPE_CONTROL_CENTER_ENTER',
    2601: 'ACTION_TYPE_INNER_NOTICE_GET',
    2701: 'ACTION_TYPE_DO_SLOTGAME',
    3001: 'ACTION_TYPE_TEAM_EDIT',
    3002: '强化英雄',
    3003: '进化英雄',
    3004: '出售卡片',
    3005: '卡组编成',
    3006: 'unit收藏',
    3007: '试炼deck编辑',
    3008: '获取试炼deck',
    4002: '任务开始',
    4003: '任务结束',
    4004: '战斗复活',
    4005: '任务重开',
    4010: 'ACTION_TYPE_GET_CHLNG_MISSION_INFO',
    4011: 'ACTION_TYPE_CHLNG_MISSION_START',
    4012: 'ACTION_TYPE_CHLNG_MISSION_FRIEND_LIST',
    4020: '获取前线猎人排期',
    4021: 'ACTION_TYPE_FROHUN_START',
    4022: '获取前线猎人关卡数据',
    4023: 'ACTION_TYPE_FROHUN_MISSION_START',
    4024: '前线猎人好友列表',
    4025: '领取前线猎人排名奖励',
    4101: '竞技场入场',
    4102: 'ACTION_TYPE_ARENA_MATCHING',
    4103: '竞技场对战开始',
    4104: '竞技场奖励',
    4105: '竞技场好友一览',
    4106: '竞技场重启',
    5001: '抽卡',
    5003: 'gacha一览',
    5102: '商店使用',
    5103: '购买钻石',
    5104: 'coin购买开始',
    7101: '礼物一览获得',
    7102: '礼物领取',
    7201: '活动领取',
    8001: 'ACTION_TYPE_MODEL_CHANGE_ID_ISSUE',
    8002: 'ACTION_TYPE_MODEL_CHANGE_ID_CHECK',
    8003: 'ACTION_TYPE_MODEL_CHANGE_END',
    9999: 'debug',
    10001: '无',
    10002: '获取RAID副本世界信息',
    10003: 'RAID副本中购买商品',
    10004: 'ACTION_TYPE_RAID_UPDATE_SCENARIO_INFO',
    10005: '获取副本当前状态的信息',
    10006: '获取房间列表',
    10007: '更新房间信息',
    10008: '进入RAID副本房间',
    10009: 'RAID副本选择副本',
    10010: 'RAID副本选择好友信息',
    10011: 'RAID副本获取好友信息',
    10012: 'RAID副本进入房间内物品编辑',
    10013: '更新用户副本是否准备状态的信息',
    10014: '退出副本',
    10015: '获取房间信息',
    10016: '副本开始',
    10017: 'RAID营地开始休息',
    10018: 'RAID营地状态获取',
    10019: 'RAID营地结束休息',
    10020: '完成任务收获',
    10021: 'RAID副本物品使用',
    10022: 'ACTION_TYPE_RAID_LIMITED_ITEM_USE',
    10023: 'ACTION_TYPE_RAID_ITEM_DELETE',
    10024: 'RAID副本物品合成',
    10025: 'RAID副本物品编辑',
    10026: 'RAID副本房间任务退出',
    10027: 'RAId副本任务完成',
    10028: '获取Raid副本任务信息',
    10029: '获取RAID副本简单的信息,开启时间,限时',
    10030: 'RAID副本任务战斗开始',
    10031: 'RAID副本任务战斗重新开始（死亡）',
    10032: 'RAID副本任务战斗结束',
    10033: '获取聊天记录',
    10034: '发送聊天信息',
    10035: '清除服务器缓存',
    10036: '解散房间',
    10037: '房间踢人',
    10038: '获取RAID副本角色信息',
    10039: '获取RAID副本角色奖杯信息',
    11111: 'ACTION_TYPE_DAILY_TASK_MAIN',
    11112: '完成每日任务',
    11113: '活跃度宝箱打开',
    11123: 'ACTION_TYPE_DAILY_STAMINA_MAIN',
    11124: '每日体力获取',
    11125: '获取每日任务信息',
    14111: 'ACTION_TYPE_CHARGE_REWARD_MAIN',
    14112: '索要任务奖励获取',
    21112: 'ACTION_TYPE_BLACK_MARKET_MAIN',
    21113: '黑市物品购买',
    21114: '黑市刷新',
    61125: 'ACTION_TYPE_DAILY_STAGE_MAIN',
    81111: 'ACTION_TYPE_DOGGY_MAIN',
    81112: 'ACTION_TYPE_DOGGY_MIX',
}
TABULATE_FACILITY_ID_NAME = {1:'宝玉屋',2:'调合屋',3:'村落升级',4:'音乐屋',5:'道具仓库'}
TABULATE_LOCATION_ID_NAME = {1:'山',2:'川',3:'田',4:'森'}
TABULATE_ARENA_CHALLENGE_RESULT_NAME = {0:'失败',1:'成功',2:'未完成'}
TABULATE_DUNGEON_KEY_DO_TYPE_NAME = {1:'产出',2:'消耗'}
TABULATE_BM_REFRESH_MONEY_TYPE_NAME = {1:'钻石'}
TABULATE_BM_BUY_MONEY_TYPE_NAME = {1:'钻石',2:'金币'}

TABULATE_DUNGEON_SLIVER_KEY_CODE = 1
TABULATE_DUNGEON_GOLD_KEY_CODE = 2

# tabulate monitor
TABULATE_MONITOR_VIP_CHANNEL_ID_NAME = TABULATE_CHANNEL_NAME