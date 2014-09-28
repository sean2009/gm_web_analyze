# -*- coding: utf-8 -*-
from django.core.management.base import BaseCommand
from django.conf import settings
from optparse import make_option
import datetime

class Command(BaseCommand):
    def handle(self, *args, **options): 
        return




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
