# register/admin.py
from django.contrib import admin
from .models import DepositRegister, SavingRegister, MortgageRegister

admin.site.register(DepositRegister)
admin.site.register(SavingRegister)
admin.site.register(MortgageRegister)