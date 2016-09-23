from django.shortcuts import render, redirect
from django.contrib import messages
from ..log_reg.models import User
from django.core.urlresolvers import reverse
import datetime
from django.utils import timezone

def index(request):
	return render(request, 'cool_app/index.html')