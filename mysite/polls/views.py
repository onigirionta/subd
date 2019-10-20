from datetime import datetime
from decimal import Decimal

from django.shortcuts import render
from django.core.serializers import serialize

# Create your views here.
from django.http import HttpResponse
import json

from .models import Futures, Trades

format_date = '%Y-%m-%d'


def futures(request):
    if request.method == 'GET':
        fs = serialize('json', Futures.objects.all())
        return HttpResponse(f'{{"data": {fs}}}')
    elif request.method == 'POST':
        body = json.load(request)
        name = body['name']
        code = body['code']
        date = datetime.strptime(body['date'], format_date)
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
        date = datetime.strptime(body['date'], format_date)
        Futures.objects.filter(name=name).update(name=new_name, base=code, exec_date=date)
        return HttpResponse('futures updated')


def trades(request):
    if request.method == 'GET':
        ts = serialize('json', Trades.objects.all())
        return HttpResponse(f'{{"data": {ts}}}')
    elif request.method == 'POST':
        body = json.load(request)
        name = body['name']
        torg_date = datetime.strptime(body['torg_date'], format_date)
        day_end = datetime.strptime(body['day_end'], format_date)
        quotation = Decimal(body['quotation'])
        max_quot = Decimal(body['max_quot'])
        min_quot = Decimal(body['min_quot'])
        num_contr = int(body['num_contr'])
        trades = Trades(name=name, torg_date=torg_date, day_end=day_end, quotation=quotation, max_quot=max_quot,
                        min_quot=min_quot, num_contr=num_contr)
        trades.save()
        return HttpResponse('trade created')
    else:
        pass  # TODO: error


def modify_trades(request, torg_date, name):
    torg_date = datetime.strptime(torg_date, format_date)

    if request.method == 'DELETE':
        Trades.objects.filter(name=name, torg_date=torg_date).delete()
        return HttpResponse('trade deleted')

    elif request.method == 'PUT':
        body = json.load(request)
        new_name = body['name']
        new_torg_date = datetime.strptime(body['torg_date'], format_date)
        day_end = datetime.strptime(body['day_end'], format_date)
        quotation = Decimal(body['quotation'])
        max_quot = Decimal(body['max_quot'])
        min_quot = Decimal(body['min_quot'])
        num_contr = int(body['num_contr'])
        Trades.objects.filter(name=name, torg_date=torg_date).update(name=new_name, torg_date=new_torg_date,
                                                                     day_end=day_end, quotation=quotation,
                                                                     max_quot=max_quot, min_quot=min_quot,
                                                                     num_contr=num_contr)
        return HttpResponse('trade updated')


def get_all_date(table):
    return json.loads(serialize('json', table))


def check_input_futures(body):  # проверка ввода данных фьючерса
    code = body['code']

    flag = check_name_correctness(body['name']) # проверка имени фьючерса
    if flag:
        return flag

    name = body['name'].split('-')

    flag = check_date_correctness(body['date']) # проверка даты
    if flag:
        return flag

    date = body['date'].split('-')

    if not (code.upper().startswith('SU') and code.upper().endswith('RMFS') and code[2:7].isnumeric()):  # проверка кода
        return 'code incorrect'

    if name[0] not in code:  # проверка совподения кода и имени фьючерса
        return 'code or name incorrect'

    if len(date[2]) == 1:           # редактирование даты
        date[2] = '0' + date[2]
        if len(date[1]) == 1:
            date[1] = '0' + date[1]

    if name[1] != date[2] + date[1] + date[0][2:]:  # проверка совподания части имени и даты
        return 'date or name incorrect'

    if Futures.objects.filter(name=body['name']).exists():  # проверка существования записи
        return 'record already exists'

    return False


def check_input_trades(body):  # проверка корректности данных торгов
    flag = check_name_correctness(body['name'])  # проверка корректности имени фьючерса
    if flag:
        return flag

    if not Futures.objects.filter(name=body['name']).exists():  # проверка существования данных фьючерса
        return 'futures does not exist'

    flag = check_date_correctness(body['torg_date'])   # проверка корректности даты торгов
    if flag:
        return flag
    elif Futures.objects.filter(name=body['name']).values()[0]['exec_date'] < datetime.strptime(
            body['torg_date'], format_date):
        return 'torg date late exec date'
    elif Trades.objects.filter(name=body['name'], torg_date=datetime.strptime(body['torg_date'], format_date)).exists():
        return 'torg date already exist'

    flag = check_date_correctness(body['day_end'])  # проверка корректности даты окончания
    if flag:
        return flag
    elif Futures.objects.filter(name=body['name']).values()[0]['exec_date'] > datetime.strptime(body['day_end'],
                                                                                                format_date):
        return 'exec date late day end'
    elif Trades.objects.filter(name=body['name']).exists():
        if Trades.objects.filter(name=body['name']).values()[0]['day_end'] == datetime.strptime(body['day_end'],
                                                                                                format_date):
            return 'day end does not match data'

    if not isfloat(body['quotation']):  # проверка значения текущей цены
        return 'quotation not a number'
    elif not 0 < Decimal(body['quotation']) <= 100:
        return 'quotation incorrect'

    if not isfloat(body['max_quot']):  # проверка максимальной цены
        return 'max quotation not a number'
    if not 0 < Decimal(body['max_quot']) <= 100:
        return 'max quotation incorrect'

    if not isfloat(body['min_quot']):  # проверка минимальной цены
        return 'min quotation not a number'
    if not 0 < Decimal(body['max_quot']) <= 100:
        return 'min quotation incorrect'

    if Decimal(body['max_quot']) < Decimal(body['min_quot']):  # проверка корректность данных
        return 'min quotation more max quotation'

    if not body['num_contr'].isdigit():  # проверка числа торгов
        return 'num contr not a number'

    return False


def check_date_correctness(date):  # проверка корректности даты
    try:
        datetime.strptime(date, format_date)
        if datetime(1800, 1, 1) < datetime.strptime(date, format_date):
            return False
        else:
            return 'early date'
    except ValueError:
        return 'date incorrect'


def check_name_correctness(name):  # проверка корректности имени фьючерса

    if '-' not in name:
        return 'missing dash'

    name = name.split('-')

    if len(name[0]) != 5 or len(name[1]) != 6:
        return 'name incorrect'
    if not (name[0].isdigit() and name[1].isdigit()):
        return 'name dose not consist of numbers'

    return False


def isfloat(value):  # проверка на то что строка это дробное число
    try:
        float(value)
        return True
    except ValueError:
        return False
