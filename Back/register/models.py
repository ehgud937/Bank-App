# register/models.py
from django.db import models
from django.conf import settings
from products.models import (
    DepositProducts, DepositOptions,
    SavingProducts, SavingOptions,
    MortgageProducts, MortgageOtions
)

class RegisterStatus(models.TextChoices):
    PENDING = 'PENDING', '신청중'
    ACTIVE = 'ACTIVE', '가입완료'
    EXPIRED = 'EXPIRED', '만기'
    CANCELLED = 'CANCELLED', '해지'

class DepositRegister(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='deposit_registers')
    product = models.ForeignKey(DepositProducts, on_delete=models.CASCADE, related_name='registers')
    option = models.ForeignKey(DepositOptions, on_delete=models.CASCADE, related_name='registers')
    status = models.CharField(max_length=10, choices=RegisterStatus.choices, default=RegisterStatus.PENDING)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

class SavingRegister(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='saving_registers')
    product = models.ForeignKey(SavingProducts, on_delete=models.CASCADE, related_name='registers')
    option = models.ForeignKey(SavingOptions, on_delete=models.CASCADE, related_name='registers')
    status = models.CharField(max_length=10, choices=RegisterStatus.choices, default=RegisterStatus.PENDING)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

class MortgageRegister(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='mortgage_registers')
    product = models.ForeignKey(MortgageProducts, on_delete=models.CASCADE, related_name='registers')
    option = models.ForeignKey(MortgageOtions, on_delete=models.CASCADE, related_name='registers')
    status = models.CharField(max_length=10, choices=RegisterStatus.choices, default=RegisterStatus.PENDING)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']