# recommendations/serializers.py
from rest_framework import serializers
from .models import ProductRecommendation

class RecommendationSerializer(serializers.ModelSerializer):
    product_name = serializers.SerializerMethodField()
    bank_name = serializers.SerializerMethodField()
    interest_info = serializers.SerializerMethodField()

    class Meta:
        model = ProductRecommendation
        fields = (
            'id', 'product_type', 'product_name', 'bank_name',
            'interest_info', 'confidence_score', 'rank',
            'recommendation_type', 'created_at'
        )

    def get_product_name(self, obj):
        if obj.deposit_product:
            return obj.deposit_product.fin_prdt_nm
        elif obj.saving_product:
            return obj.saving_product.fin_prdt_nm
        elif obj.mortgage_product:
            return obj.mortgage_product.fin_prdt_nm
        return None

    def get_bank_name(self, obj):
        if obj.deposit_product:
            return obj.deposit_product.kor_co_nm
        elif obj.saving_product:
            return obj.saving_product.kor_co_nm
        elif obj.mortgage_product:
            return obj.mortgage_product.kor_co_nm
        return None

    def get_interest_info(self, obj):
        if obj.deposit_product:
            options = obj.deposit_product.depositoptions_set.all()
            return {
                'basic_rate': options[0].intr_rate if options else None,
                'max_rate': options[0].intr_rate2 if options else None
            }
        elif obj.saving_product:
            options = obj.saving_product.savingoptions_set.all()
            return {
                'basic_rate': options[0].intr_rate if options else None,
                'max_rate': options[0].intr_rate2 if options else None
            }
        elif obj.mortgage_product:
            options = obj.mortgage_product.mortgageotions_set.all()
            return {
                'min_rate': options[0].lend_rate_min if options else None,
                'max_rate': options[0].lend_rate_max if options else None
            }
        return None