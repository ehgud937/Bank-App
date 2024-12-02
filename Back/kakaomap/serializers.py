# kakaomap/serializers.py
from rest_framework import serializers
from .models import BankStore

class BankStoreSerializer(serializers.ModelSerializer):
    class Meta:
        model = BankStore
        fields = '__all__'