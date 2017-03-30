"""
Module for storing data about user's money, payments and user's transaction history"""

from __future__ import unicode_literals

from django.db import models

from bitjobs.settings import CURRENCIES


class Wallet(models.Model):
    def save(self, *args, **kwargs):
        super(Wallet, self ).save(*args, **kwargs)
        for (c, c2) in CURRENCIES:
            CurrencyAccount.objects.create(currency=c, amount=0, wallet=self)


# Unfortunately django-money does not allow selecting specific currency, so I'm rolling my own solution
class CurrencyAccount(models.Model):
    currency = models.CharField(choices=CURRENCIES, max_length=3)
    amount = models.DecimalField('amount', 'amount', 10, 2)
    wallet = models.ForeignKey(Wallet, on_delete=models.CASCADE)
