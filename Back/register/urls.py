# register/urls.py
from django.urls import path
from . import views

app_name = 'register'

urlpatterns = [
    path('deposit/<int:product_id>/<int:option_id>/', views.register_deposit),
    path('saving/<int:product_id>/<int:option_id>/', views.register_saving),
    path('mortgage/<int:product_id>/<int:option_id>/', views.register_mortgage),
    path('my-registers/', views.user_registers),
    path('cancel/<str:register_type>/<int:register_id>/', views.cancel_register),
]