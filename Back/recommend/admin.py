# recommendations/admin.py
from django.contrib import admin
from .models import ProductRecommendation

admin.site.register(ProductRecommendation)