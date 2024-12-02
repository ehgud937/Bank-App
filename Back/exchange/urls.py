# exchange/urls.py

from django.urls import path
from . import views

app_name = 'exchange'

urlpatterns = [
   path('test/', views.index),
   path('save-exchange-rate/', views.save_exchange),
   path('exchange-get-all/', views.exchange_get_all,)
]