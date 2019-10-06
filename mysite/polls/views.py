from datetime import datetime

from django.shortcuts import render
from django.core.serializers import serialize

# Create your views here.
from django.http import HttpResponse
import json

from .models import Futures, Trades

def futures(request):
    if request.method == 'GET':
        fs = serialize('json', Futures.objects.all())
        return HttpResponse(f'{{"data": {fs}}}')
    elif request.method == 'POST':
        body = json.load(request)
        name = body['name']
        code = body['code']
        date = datetime.strptime(body['date'], '%Y-%m-%d')
        futures = Futures(name=name, base=code, exec_date=date)
        futures.save()
        return HttpResponse('futures created')
    else:
        pass  # TODO: error

def modify_futures(request, name):
    if request.method == 'DELETE':
        Futures.objects.filter(name=name).delete()
        return HttpResponse('futures deleted')
    elif request.method == 'PUT':
        body = json.load(request)
        new_name = body['name']
        code = body['code']
        date = datetime.strptime(body['date'], '%Y-%m-%d')
        Futures.objects.filter(name=name).update(name=new_name, base=code, exec_date=date)
        return HttpResponse('futures updated')

def trades(request):
    ts = serialize('json', Trades.objects.all())
    return HttpResponse(f'{{"data": {ts}}}')
