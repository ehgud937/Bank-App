# register/serializers.py
from rest_framework import serializers
from .models import DepositRegister, SavingRegister, MortgageRegister
from products.serializers import (
    DepositProductWithOptionSerialzier,
    SavingProductWithOptionSerialzier,
    MortgageProductWithOptionSerialzier
)

class DepositRegisterSerializer(serializers.ModelSerializer):
    product_info = DepositProductWithOptionSerialzier(source='product', read_only=True)

    class Meta:
        model = DepositRegister
        fields = '__all__'
        read_only_fields = ('user',)

class SavingRegisterSerializer(serializers.ModelSerializer):
    product_info = SavingProductWithOptionSerialzier(source='product', read_only=True)

    class Meta:
        model = SavingRegister
        fields = '__all__'
        read_only_fields = ('user',)

class MortgageRegisterSerializer(serializers.ModelSerializer):
    product_info = MortgageProductWithOptionSerialzier(source='product', read_only=True)

    class Meta:
        model = MortgageRegister
        fields = '__all__'
        read_only_fields = ('user',)