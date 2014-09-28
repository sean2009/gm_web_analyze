# -*- coding: utf-8 -*-

import datetime

from gna.common import (
    date_range_since_up,
)
from gna.models import (
    DailyCache,
    SimpleCache,
    DeltaCache,
    DailyFlagCache
)

class cache(object):
    MODEL = ''

    def get(self, db, **query):
        return eval(self.MODEL).objects.using(db).filter(**query).values()

    def set(self, db, value_dict, **query):
        obj, created = eval(self.MODEL).objects.using(db).update_or_create(defaults=value_dict, **query)
        return obj

class daily_cache(cache):
    MODEL = 'DailyCache'

    def get(self, db, key, date):
        value = super(daily_cache, self).get(db, key=key, date=date)
        return value[0] if value else None

    def get_by_date_list(self, db, key, date_list):
        return super(daily_cache, self).get(db, key=key, date__in=date_list)

    def get_by_date_range(self, db, key, from_date, to_date):
        return super(daily_cache, self).get(db, key=key, date__range=(from_date, to_date))

    def set(self, db, key, date, value):
        return super(daily_cache, self).set(db, {'value':value}, key=key, date=date)

class simple_cache(cache):
    MODEL = 'SimpleCache'

    def get(self, db, key):
        value = super(simple_cache, self).get(db, key=key)
        return value[0] if value else None

    def set(self, db, key, value):
        return super(simple_cache, self).set(db, {'value':value}, key=key)

class delta_cache(cache):
    MODEL = 'DeltaCache'

    def get(self, db, key):
        value = super(delta_cache, self).get(db, key=key)
        return value[0] if value else None

    def set(self, db, key, datetime, value):
        return super(delta_cache, self).set(db, {'datetime':datetime, 'value':value}, key=key)

class daily_flag_cache(cache):
    MODEL = 'DailyFlagCache'

    def get(self, db, key, date):
        value = super(daily_flag_cache, self).get(db, key=key, date=date)
        return value[0] if value else None

    def get_uncached_dates(self, db, key):
        result = date_range_since_up(db)
        cached_docs = super(daily_flag_cache, self).get(db, key=key)
        for doc in cached_docs:
            the_date = doc['date']
            if the_date in result:
                result.remove(the_date)
        return result

    def set(self, db, key, date, value):
        return super(daily_flag_cache, self).set(db, {'value':value}, key=key, date=date)


