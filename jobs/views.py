from django.shortcuts import render
from django.http.response import HttpResponse
from jobs.models import Registration
import json


def add_register_job(request):
    return render(request, 'frontend/base.html')
