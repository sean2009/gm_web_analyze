# -*- coding: utf-8 -*-

from django.core.management.base import BaseCommand
from django.conf import settings
from optparse import make_option
import atexit
import datetime

from gna.cache import simple_cache
from gna.update import update_cache
from gna.common import str_to_date
from gna.repair import repair

class Command(BaseCommand):
    option_list = BaseCommand.option_list + (
        make_option(
            "--date",
            dest='date', 
            default=False,
            help='%%Y-%%m-%%d.'
        ),
        make_option(
            "--db",
            dest='db',
            default=False,
            help='default: all dbs.'
        )
    )

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

        date_list = []
        if options['date']:
            try:
                the_date = str_to_date(options['date'])
                date_list.append(the_date)
            except:
                print 'date error!'
                return 
        else:
            print 'no date!'         
   
        dbs = []
        if options['db']:
            if options['db'] in settings.GNA_DATABASES:
                dbs.append(options['db'])
            else:
                print 'db error!'
                return 
        else:
            dbs = settings.GNA_DATABASES
       
        print 'repair db:%s\n       date:%s' % (dbs, date_list)
        time_counter = Time_counter()
        print 'repair gna begin : %s' % str(datetime.datetime.now())
        repair(date_list, dbs)
        print 'repair gna end   : %s' % str(datetime.datetime.now())
        print 'repair gna use time : %s' % str(time_counter.get())
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
