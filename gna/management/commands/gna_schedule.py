# -*- coding: utf-8 -*-

from django.core.management.base import BaseCommand
import atexit
import datetime

from gna.cache import simple_cache
from gna.update import update_cache

class Command(BaseCommand):
    @staticmethod
    def lock_db_name():
        return 'default'
        
    @staticmethod
    def lock_cache_key():
        return 'GNA_SCHEDULE_LOCK'

    @staticmethod
    def lock():
        lock_cache_key = Command.lock_cache_key()
        lock_db_name = Command.lock_db_name()
        if simple_cache().get(lock_db_name, lock_cache_key)['value'] == 'unlock':
            simple_cache().set(lock_db_name, lock_cache_key, 'lock')
            atexit.register(Command.unlock)
            return True
        else:
            print 'lock command error!'
            return False

    @staticmethod
    def unlock():
        simple_cache().set(Command.lock_db_name(), Command.lock_cache_key(), 'unlock')

    def handle(self, *args, **options):
    	print '#'*80

        if not Command.lock():
            print 'gna lock!'
            return False

        time_counter = Time_counter()
        print 'update cache begin : %s' % str(datetime.datetime.now())
        update_cache()     
        print 'update cache end : %s' % str(datetime.datetime.now())
        print 'update cache use time : %s' % str(time_counter.get())

        print '#'*80





class Time_counter:
    def __init__(self):
        self.time_begin = datetime.datetime.now()
        self.time =  datetime.datetime.now()

    def set(self):
        self.time_begin = datetime.datetime.now()
        self.time = datetime.datetime.now()

    def get(self):
        time_delta = datetime.datetime.now() - self.time
        self.time = datetime.datetime.now()
        return time_delta

    def get_counter(self):
        return datetime.datetime.now() - self.time_begin
