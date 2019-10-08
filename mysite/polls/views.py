from datetime import datetime
from decimal import Decimal

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
        quotation = Decimal(body['quotation'])
        max_quot = Decimal(body['max_quot'])
        min_quot = Decimal(body['min_quot'])
        num_contr = int(body['num_contr'])
        trades = Trades(name=name, torg_date=torg_date, day_end=day_end, quotation=quotation, max_quot=max_quot, min_quot=min_quot, num_contr=num_contr)
        trades.save()
        return HttpResponse('trade created')
    else:
        pass  # TODO: error

def modify_trades(request, torg_date, name):
    torg_date = datetime.strptime(torg_date, '%Y-%m-%d')

    if request.method == 'DELETE':    
        Trades.objects.filter(name=name, torg_date=torg_date).delete()
        return HttpResponse('trade deleted')
    
    elif request.method == 'PUT':
        body = json.load(request)
        new_name = body['name']
        new_torg_date = datetime.strptime(body['torg_date'], '%Y-%m-%d')
        day_end = datetime.strptime(body['day_end'], '%Y-%m-%d')        
        quotation = Decimal(body['quotation'])
        max_quot = Decimal(body['max_quot'])
        min_quot = Decimal(body['min_quot'])
        num_contr = int(body['num_contr'])
        Trades.objects.filter(name=name, torg_date=torg_date).update(name=new_name, torg_date=new_torg_date, day_end=day_end, quotation=quotation, max_quot=max_quot, min_quot=min_quot, num_contr=num_contr)
        return HttpResponse('trade updated')