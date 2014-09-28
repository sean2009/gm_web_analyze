# -*- coding: utf-8 -*-

from django.core.management.base import BaseCommand
from django.conf import settings
import datetime

from gna.models import (
    DailyCache,
    SimpleCache,
    DeltaCache,
    DailyFlagCache,
)

class Command(BaseCommand):
    def handle(self, *args, **options):
        for db in settings.GNA_DATABASES:
            SimpleCache.objects.using(db).all().delete()
            DailyCache.objects.using(db).all().delete()
            DeltaCache.objects.using(db).all().delete()
            DailyFlagCache.objects.using(db).all().delete()
        
        SimpleCache.objects.using('default').all().delete()
        SimpleCache.objects.using('default').create(key='GNA_SCHEDULE_LOCK', value='unlock')




