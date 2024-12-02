# products/urls.py
from django.urls import path
from . import views

app_name = 'products'

urlpatterns = [
    path('test-deposit/', views.index),
    path('save-deposit-products/', views.save_deposit_product, name='save_deposit_product'),
    path('deposit-products/', views.deposit_products, name='deposit_products'),
    path('deposit-product-options/<str:fin_prdt_cd>/', views.deposit_product_options, name='deposit_product_options'),
    path('deposit-products/top_rate/', views.top_rate, name='top_rate'),
    path('deposit-get-all/', views.deposit_get_all),
    path('deposit_detail/<int:pk>/', views.deposit_detail),

    path('test-saving/', views.index_saving),
    path('save-saving-products/', views.save_saving_product, name='save_saving_product'),
    path('saving-get-all/', views.saving_get_all),
    path('saving_detail/<int:pk>/', views.saving_detail),

    path('test-mortgage/', views.index_mortgage),
    path('save-mortgage-products/', views.save_mortgage_product),
    path('mortgage-get-all/', views.mortgage_get_all),
    path('mortgage_detail/<int:pk>/', views.mortgage_detail),
]