# products/admin.py
from django.contrib import admin
from .models import (
    DepositProducts, DepositOptions,
    SavingProducts, SavingOptions,
    MortgageProducts, MortgageOtions
)

admin.site.register(DepositProducts)
admin.site.register(DepositOptions)
admin.site.register(SavingProducts)
admin.site.register(SavingOptions)
admin.site.register(MortgageProducts)
admin.site.register(MortgageOtions)