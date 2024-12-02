# recommendations/models.py
from django.db import models
from django.conf import settings

class ProductRecommendation(models.Model):
    """추천 상품 기록"""
    RECOMMENDATION_TYPES = [
        ('RULE_BASED', '규칙 기반 추천'),
        ('ML_BASED', '머신러닝 기반 추천'),
        ('HIGH_RATE', '높은 금리형'),
        ('STABLE', '안정 추구형'),
        ('BALANCED', '균형형'),
        ('CUSTOM', '맞춤형')
    ]

    PRODUCT_TYPES = [
        ('DEPOSIT', '예금'),
        ('SAVING', '적금'),
        ('MORTGAGE', '주택담보대출')
    ]

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    product_type = models.CharField(max_length=10, choices=PRODUCT_TYPES)
    deposit_product = models.ForeignKey('products.DepositProducts', 
                                      on_delete=models.CASCADE, null=True, blank=True)
    saving_product = models.ForeignKey('products.SavingProducts', 
                                     on_delete=models.CASCADE, null=True, blank=True)
    mortgage_product = models.ForeignKey('products.MortgageProducts', 
                                       on_delete=models.CASCADE, null=True, blank=True)
    confidence_score = models.FloatField()
    rank = models.IntegerField()
    recommendation_type = models.CharField(max_length=20, choices=RECOMMENDATION_TYPES)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['rank']
        indexes = [
            models.Index(fields=['user', 'product_type', 'recommendation_type']),
        ]