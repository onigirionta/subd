from .models import Futures, Trades


def get_all_Futures():
    res_list = []
    for val in Futures.objects.all():
        res_list.append([val.name, val.base, val.exec_date])
    return res_list


def get_all_Trades():
    res_list = []
    for val in Trades.objects.all():
        res_list.append([val.name, val.torg_date, val.day_end, val.qutation, val.min_quot, val.min_quot, val.num_contr])
    return res_list


