from django.contrib import admin

from .models import Wallet, CurrencyAccount

admin.site.register(Wallet)
admin.site.register(CurrencyAccount)