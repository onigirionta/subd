from django.shortcuts import render
from django.core.serializers import serialize

# Create your views here.
from django.http import HttpResponse
import json

from .models import Futures, Trades

def futures(request):
    fs = serialize('json', Futures.objects.all())
    return HttpResponse(f'{{"data": {fs}}}')

def trades(request):
    ts = serialize('json', Trades.objects.all())
    return HttpResponse(f'{{"data": {ts}}}')
