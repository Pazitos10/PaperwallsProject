#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.shortcuts import render_to_response
from django.template import RequestContext
from django.http import HttpResponseRedirect

def index(request):
	return render_to_response("base.html", context_instance = RequestContext(request))