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
    if request.method == 'GET':
        ts = serialize('json', Trades.objects.all())
        return HttpResponse(f'{{"data": {ts}}}')
    elif request.method == 'POST':
        body = json.load(request)
        name = body['name']
        torg_date = datetime.strptime(body['torg_date'], '%Y-%m-%d')
        day_end = datetime.strptime(body['day_end'], '%Y-%m-%d')        
        quotation = body['quotation']
        max_quot = body['max_quot']
        min_quot = body['min_quot']
        num_contr = body['num_contr']
        trades = Trades(name=name, torg_date=torg_date, day_end=day_end, quotation=quotation, max_quot=max_quot, min_quot=min_quot, num_contr=num_contr)
        trades.save()
        return HttpResponse('trade created')
    else:
        pass  # TODO: error

def modify_trades(request, name):
    if request.method == 'DELETE':
        Trades.objects.filter(name=name, torg_date=code).delete()
        return HttpResponse('trade deleted')
    elif request.method == 'PUT':
        body = json.load(request)
        name = body['name']
        torg_date = datetime.strptime(body['torg_date'], '%Y-%m-%d')
        day_end = datetime.strptime(body['day_end'], '%Y-%m-%d')        
        quotation = body['quotation']
        max_quot = body['max_quot']
        min_quot = body['min_quot']
        num_contr = body['num_contr']
        Trades.objects.filter(name=name, torg_date=code).update(name=name, torg_date=torg_date, day_end=day_end, quotation=quotation, max_quot=max_quot, min_quot=min_quot, num_contr=num_contr)
        return HttpResponse('trade updated')