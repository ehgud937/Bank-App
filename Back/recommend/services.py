from django.db.models import Avg, F, Q
from django.db.models.functions import Abs
from products.models import DepositProducts, SavingProducts, MortgageProducts
from .ml_models import UserBasedRecommender

class FinancialRecommender:
    def __init__(self, user):
        self.user = user
        self.ml_recommender = UserBasedRecommender()

    def get_recommendations(self):
        """전체 추천 상품 조회"""
        rule_based = {
            'deposit': self._get_deposit_recommendations(),
            'saving': self._get_saving_recommendations(),
            'mortgage': self._get_mortgage_recommendations()
        }
        
        ml_based = self.ml_recommender.get_recommendations(self.user)
        
        recommendations = {
            'rule_based': rule_based,
            'ml_based': ml_based
        }
        
        return recommendations

    def _get_deposit_recommendations(self):
        """예금 상품 추천"""
        recommendations = {
            'HIGH_RATE': self._get_high_rate_deposits(),
            'STABLE': self._get_stable_deposits(),
            'BALANCED': self._get_balanced_deposits(),
            'CUSTOM': self._get_custom_deposits()
        }
        return recommendations

    def _get_saving_recommendations(self):
        """적금 상품 추천"""
        recommendations = {
            'HIGH_RATE': self._get_high_rate_savings(),
            'STABLE': self._get_stable_savings(),
            'BALANCED': self._get_balanced_savings(),
            'CUSTOM': self._get_custom_savings()
        }
        return recommendations

    def _get_mortgage_recommendations(self):
        """주택담보대출 상품 추천"""
        if self.user.assets < 100000000:  # 1억 미만
            return {}
        
        recommendations = {
            'LOW_RATE': self._get_low_rate_mortgages(),
            'STABLE': self._get_stable_mortgages(),
            'CUSTOM': self._get_custom_mortgages()
        }
        return recommendations

    def _get_high_rate_deposits(self):
        """높은 금리 예금 추천"""
        return DepositProducts.objects.filter(
            depositoptions__intr_rate__gt=0
        ).annotate(
            max_rate=Avg('depositoptions__intr_rate')
        ).order_by('-max_rate')[:3]

    def _get_stable_deposits(self):
        """안정형 예금 추천"""
        major_banks = ['KB', 'SH', 'WR', 'NH']
        return DepositProducts.objects.filter(
            kor_co_nm__in=major_banks,
            join_deny=1  # 제한없음
        )[:3]

    def _get_balanced_deposits(self):
        """균형 잡힌 예금 추천"""
        avg_rate = DepositProducts.objects.filter(
            depositoptions__intr_rate__gt=0
        ).aggregate(
            avg_rate=Avg('depositoptions__intr_rate')
        )['avg_rate']

        return DepositProducts.objects.filter(
            depositoptions__intr_rate__gt=0
        ).annotate(
            rate_diff=Abs(F('depositoptions__intr_rate') - avg_rate)
        ).order_by('rate_diff')[:3]

    def _get_custom_deposits(self):
        """맞춤형 예금 추천"""
        if self.user.investment_type == 'CONSERVATIVE':
            return self._get_stable_deposits()
        elif self.user.investment_type in ['AGGRESSIVE', 'SPECULATIVE']:
            return self._get_high_rate_deposits()
        else:
            return self._get_balanced_deposits()

    def _get_high_rate_savings(self):
        """높은 금리 적금 추천"""
        monthly_available = self.user.annual_income / 12 * 0.3
        
        return SavingProducts.objects.filter(
            savingoptions__intr_rate__gt=0
        ).annotate(
            max_rate=Avg('savingoptions__intr_rate')
        ).order_by('-max_rate')[:3]

    def _get_stable_savings(self):
        """안정형 적금 추천"""
        major_banks = ['KB', 'SH', 'WR', 'NH']
        return SavingProducts.objects.filter(
            kor_co_nm__in=major_banks,
            join_deny=1
        )[:3]

    def _get_balanced_savings(self):
        """균형 잡힌 적금 추천"""
        avg_rate = SavingProducts.objects.filter(
            savingoptions__intr_rate__gt=0
        ).aggregate(
            avg_rate=Avg('savingoptions__intr_rate')
        )['avg_rate']

        return SavingProducts.objects.filter(
            savingoptions__intr_rate__gt=0
        ).annotate(
            rate_diff=Abs(F('savingoptions__intr_rate') - avg_rate)
        ).order_by('rate_diff')[:3]

    def _get_custom_savings(self):
        """맞춤형 적금 추천"""
        if self.user.investment_type == 'CONSERVATIVE':
            return self._get_stable_savings()
        elif self.user.investment_type in ['AGGRESSIVE', 'SPECULATIVE']:
            return self._get_high_rate_savings()
        else:
            return self._get_balanced_savings()

    def _get_low_rate_mortgages(self):
        """낮은 금리 주택담보대출 추천"""
        return MortgageProducts.objects.filter(
            mortgageotions__lend_rate_min__gt=0
        ).order_by('mortgageotions__lend_rate_min')[:3]

    def _get_stable_mortgages(self):
        """안정형 주택담보대출 추천"""
        major_banks = ['KB', 'SH', 'WR', 'NH']
        return MortgageProducts.objects.filter(
            kor_co_nm__in=major_banks
        )[:3]

    def _get_custom_mortgages(self):
        """맞춤형 주택담보대출 추천"""
        if self.user.investment_type == 'CONSERVATIVE':
            return self._get_stable_mortgages()
        else:
            return self._get_low_rate_mortgages()