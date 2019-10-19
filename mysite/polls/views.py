from datetime import datetime
from decimal import Decimal

from django.shortcuts import render
from django.core.serializers import serialize

import re
# Create your views here.
from django.http import HttpResponse
import json

from .models import Futures, Trades


def futures(request):
    if request.method == 'GET':
        fs = serialize('json', Futures.objects.all())
        return HttpResponse(f'{{"data": {fs}}}')

    elif request.method == 'POST':
        try:
            body = json.load(request)
            code = body['code']
            date = datetime.strptime(body['date'], '%Y-%m-%d')
        except:
            return HttpResponse('Неверный формат данных.', status=400)

        result = validate_futures(code, date)
        if "error_message" in result:
            return HttpResponse(result["error_message"], status=result["error_code"])

        try:
            futures = Futures(name=result["name"], base=code, exec_date=date)
            futures.save()
            return HttpResponse(status=201)
        except:
            return HttpResponse('Ошибка базы данных.', status=500)

    else:
        return HttpResponse('Недопустимый глагол HTTP.', status=405)


def modify_futures(request, name):
    if request.method == 'DELETE':
        try:
            if Trades.objects.filter(name=name).count():
                return HttpResponse('Нельзя удалить фьючерс с торгами.', status=409)
            Futures.objects.filter(name=name).delete()
        except:
            return HttpResponse('Ошибка базы данных.', status=500)
        return HttpResponse(status=201)

    elif request.method == 'PUT':
        try:
            body = json.load(request)
            code = body['code']
            date = datetime.strptime(body['date'], '%Y-%m-%d')
        except:
            return HttpResponse('Неверный формат данных.', status=400)

        result = validate_futures(code, date, name)
        if "error_message" in result:
            return HttpResponse(result["error_message"], status=result["error_code"])

        if "name" not in result:
            return HttpResponse(status=201)

        try:
            if Trades.objects.filter(name=name).count():
                return HttpResponse('Нельзя изменить фьючерс с торгами.', status=409)
            Futures.objects.filter(name=name).update(name=result["name"], base=code, exec_date=date)
        except:
            return HttpResponse('Ошибка базы данных.', status=500)
    
        return HttpResponse(status=201)

    else:
        return HttpResponse('Недопустимый глагол HTTP.', status=405)


def validate_futures(code, date, old_name=''):
    val = re.findall('^SU([0-9]{5})RMFS$', code)
    if not val:
        return {
            "error_message": 'Нужен пятизначный код серии.',
            "error_code": 422,
        }

    name = val[0] + date.strftime('-%d%m') + date.strftime('%Y')[2:]
    if name == old_name:
        return {}

    f = Futures.objects.filter(name=name)
    if f:
        return {
            "error_message": 'Такой фьючерс уже есть.',
            "error_code": 409,
        }

    return {"name": name}


def trades(request):
    if request.method == 'GET':
        ts = serialize('json', Trades.objects.all())
        return HttpResponse(f'{{"data": {ts}}}')

    elif request.method == 'POST':
        try:
            body = json.load(request)
            name = body['name']
            torg_date = datetime.strptime(body['torg_date'], '%Y-%m-%d')
            day_end = datetime.strptime(body['day_end'], '%Y-%m-%d')        
            quotation = Decimal(body['quotation'])
            max_quot = Decimal(body['max_quot'])
            min_quot = Decimal(body['min_quot'])
            num_contr = int(body['num_contr'])
        except:
            return HttpResponse('Неверный формат данных.', status=400)

        error = vailidate_trade(name, torg_date, day_end, quotation, max_quot, min_quot, num_contr)
        if error:
            return HttpResponse(error, status=422)

        trades = Trades(name=name, torg_date=torg_date, day_end=day_end, quotation=quotation, max_quot=max_quot, min_quot=min_quot, num_contr=num_contr)
        trades.save()
        return HttpResponse(status=201)

    else:
        return HttpResponse('Недопустимый глагол HTTP.', status=405)


def modify_trades(request, torg_date, name):
    torg_date = datetime.strptime(torg_date, '%Y-%m-%d')

    if request.method == 'DELETE':    
        Trades.objects.filter(name=name, torg_date=torg_date).delete()
        return HttpResponse(status=201)
    
    elif request.method == 'PUT':
        try:
            body = json.load(request)
            new_name = body['name']
            new_torg_date = datetime.strptime(body['torg_date'], '%Y-%m-%d')
            day_end = datetime.strptime(body['day_end'], '%Y-%m-%d')        
            quotation = Decimal(body['quotation'])
            max_quot = Decimal(body['max_quot'])
            min_quot = Decimal(body['min_quot'])
            num_contr = int(body['num_contr'])
        except:
            return HttpResponse('Неверный формат данных.', status=400)
            
        error = vailidate_trade(new_name, new_torg_date, day_end, quotation, max_quot, min_quot, num_contr)
        if error:
            return HttpResponse(error, status=422)

        Trades.objects.filter(name=name, torg_date=torg_date).update(name=new_name, torg_date=new_torg_date, day_end=day_end, quotation=quotation, max_quot=max_quot, min_quot=min_quot, num_contr=num_contr)
        return HttpResponse(status=201)

    else:
        return HttpResponse('Недопустимый глагол HTTP.', status=405)


def vailidate_trade(name, torg_date, day_end, quotation, max_quot, min_quot, num_contr):
    if quotation <= 0:
        return 'Цена должна быть больше 0.'
    if num_contr < 0:
        return 'Количество проданных должно быть не меньше 0.'
    if min_quot < 0:
        return 'Минимальная цена должна быть не меньше 0.'
    if max_quot < 0:
        return 'Максимальная цена должна быть не меньше 0.'
    if min_quot > max_quot:
        return 'Минимальная цена не должна превышать максимальную.'
    if torg_date > day_end:
        return 'Торг не может быть позже погашения фьючерса.'

    needed_futures = Futures.objects.filter(name=name)
    if not needed_futures:
        return 'Нет такого фьючерса.'
    if torg_date.date() > needed_futures[0].exec_date:
        return 'Торг не может быть позже исполнения фьючерса.'
    if day_end.date() > needed_futures[0].exec_date:
        return 'Погашение не может быть позже исполнения фьючерса.'