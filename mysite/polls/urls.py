from django.urls import path

from . import views

urlpatterns = [
    path('futures', views.futures, name='futures'),
    path('trades', views.trades, name='trades'),
]