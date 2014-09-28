# -*- coding: utf-8 -*-

from django.contrib.auth.decorators import login_required
from django.shortcuts import render_to_response
from django.template import RequestContext

from django.conf import settings

@login_required
def index(request):
    ctxt = RequestContext(request, {})
    return render_to_response('gna/index.html', ctxt)

def logout(request):
    from django.contrib.auth.views import logout
    return logout(request)