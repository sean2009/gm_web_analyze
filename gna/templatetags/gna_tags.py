# -*- coding: utf-8 -*-

from django import template
from django.contrib.humanize.templatetags.humanize import intcomma
from django.conf import settings

from collections import defaultdict

register = template.Library()

