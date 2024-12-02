# kakaomap/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('search/', views.bank_search, name='bank_search'),
    path('nearby/', views.nearby_banks, name='nearby_banks'),
]