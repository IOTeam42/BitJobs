"""
Module for storing data about user's money, payments and user's transaction history"""

from __future__ import unicode_literals

from django.db import models, transaction
from django.core import validators

from bitjobs.settings import CURRENCIES

class CannotTransfer(Exception):
    def __init__(self, message):
        super(CannotTransfer, self).__init__(message)


def valid_currency(name):
    return name in [currency for (currency, _) in CURRENCIES]


class Wallet(models.Model):
    def save(self, *args, **kwargs):
        super(Wallet, self ).save(*args, **kwargs)
        for (c, c2) in CURRENCIES:
            CurrencyAccount.objects.create(currency=c, amount=0, wallet=self)

    def _currency_account_by_currency(self, currency):
        return self.currencyaccount_set.filter(currency__exact=currency).first()

    def money_by_currency(self, currency:str):
        if not valid_currency(currency):
            raise ValueError("Invalid currency name: '%s'" % currency)
        return self._currency_account_by_currency(currency).amount

    #TODO: Shouldn't that go somewhere else?
    def transfer(self, target, currency, quantity):
        if not valid_currency(currency):
            raise ValueError("Invalid currency name '%s'" % currency)

        source_currency_account = self._currency_account_by_currency(currency)
        money = source_currency_account.amount
        if money < quantity:
            raise CannotTransfer("Insufficient money, needs %d %s, have only %d %s" % (quantity, currency,money, currency ))

        target_currency_account = target._currency_account_by_currency(currency)

        with transaction.atomic():
            target_currency_account.amount += quantity
            target_currency_account.save()
            source_currency_account.amount -= quantity
            source_currency_account.save()


# Unfortunately django-money does not allow selecting specific currency, so I'm rolling my own solution
class CurrencyAccount(models.Model):
    currency = models.CharField(choices=CURRENCIES, max_length=3)
    amount = models.DecimalField(max_digits=10, decimal_places=2, validators=[validators.MinValueValidator(0)], default=0)
    wallet = models.ForeignKey(Wallet, on_delete=models.CASCADE)
