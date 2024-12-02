from rest_framework import serializers
from .models import DepositOptions, DepositProducts, SavingProducts, SavingOptions, MortgageOtions, MortgageProducts

# 예금 상품 serializer
class DepositProductsSerializer(serializers.ModelSerializer):
    class Meta:
        model = DepositProducts
        fields = '__all__'

# 예금 상품 Option serialzier
class DepositOptionsSerializer(serializers.ModelSerializer):

    class Meta:
        model = DepositOptions
        fields = '__all__'
        read_only_fields = ('product',)

# 적금 상품 Serializer
class SavingProductsSerializer(serializers.ModelSerializer):
    class Meta:
        model = SavingProducts
        fields = '__all__'

# 적금 상품 Option serialzier
class SavingOptionsSerializer(serializers.ModelSerializer):

    class Meta:
        model = SavingOptions
        fields = '__all__'
        read_only_fields = ('product',)


# 주택담보 상품 Serializer
class MortgageProductsSerializer(serializers.ModelSerializer):
    class Meta:
        model = MortgageProducts
        fields = '__all__'

# 주택담보 상품 Option serialzier
class MortgageOptionsSerializer(serializers.ModelSerializer):

    class Meta:
        model = MortgageOtions
        fields = '__all__'
        read_only_fields = ('product',)


class DepositProductWithOptionSerialzier(serializers.ModelSerializer):
    class OptionForDepositSerializer(serializers.ModelSerializer):
        class Meta:
            model = DepositOptions
            fields = '__all__'
    
    options = OptionForDepositSerializer(many=True, source='depositoptions_set')

    class Meta:
        model = DepositProducts
        fields = '__all__'

class SavingProductWithOptionSerialzier(serializers.ModelSerializer):
    class OptionForSavingSerializer(serializers.ModelSerializer):
        class Meta:
            model = SavingOptions
            fields = '__all__'
    
    options = OptionForSavingSerializer(many=True, source='savingoptions_set')

    class Meta:
        model = SavingProducts
        fields = '__all__'

class MortgageProductWithOptionSerialzier(serializers.ModelSerializer):
    class OptionForMortgageSerializer(serializers.ModelSerializer):
        class Meta:
            model = MortgageOtions
            fields = '__all__'
    
    options = OptionForMortgageSerializer(many=True, source='mortgageotions_set')
    class Meta:
        model = MortgageProducts
        fields = '__all__'