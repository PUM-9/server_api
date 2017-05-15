from django.shortcuts import render
from django.http.response import HttpResponse
from jobs.models import Registration
import json


def hello_world(request):
    return HttpResponse('Hello world!')
