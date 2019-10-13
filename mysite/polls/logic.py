from .models import Futures, Trades
from django.core.serializers import serialize
import json


def get_all_date(table):
    return json.loads(serialize('json', table.objects.all()))





