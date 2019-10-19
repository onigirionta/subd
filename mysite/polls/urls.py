from django.urls import path

from . import views

urlpatterns = [
    path('futures', views.futures, name='futures'),
    path('futures/<name>', views.modify_futures),
    path('trades', views.trades, name='trades'),
    path('trades/<torg_date>/<name>', views.modify_trades),
    path('report', views.report, name='report'),
]