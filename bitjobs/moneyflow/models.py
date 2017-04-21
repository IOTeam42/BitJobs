"""
Module for storing data about user's money, payments and user's transaction history"""

from __future__ import unicode_literals

from decimal import Decimal

from bitjobs.settings import CURRENCIES_CHOICE
from django.contrib.auth.models import User
from django.core import validators
from django.db import models
from django.db.models.signals import post_save


class CannotTransfer(Exception):
    def __init__(self, message):
        super(CannotTransfer, self).__init__(message)


def valid_currency(name):
    return name in [currency for (currency, _) in CURRENCIES_CHOICE]


class Wallet(models.Model):
    def save(self, *args, **kwargs):
        super(Wallet, self).save(*args, **kwargs)
        for (c, c2) in CURRENCIES_CHOICE:
            if not self.currencyaccount_set.filter(currency=c).exists():
                CurrencyAccount.objects.create(currency=c, amount=0, wallet=self)

    def _currency_account_by_currency(self, currency):
        return self.currencyaccount_set.filter(currency__exact=currency).first()

    def money_by_currency(self, currency: str):
        if not valid_currency(currency):
            raise ValueError("Invalid currency name: '%s'" % currency)
        return self._currency_account_by_currency(currency).amount

    # TODO: Shouldn't that go somewhere else?
    def change(self, currency, quantity):
        if not valid_currency(currency):
            raise ValueError("Invalid currency name '%s'" % currency)

        quantity = Decimal(float(quantity))
        source_currency_account = self._currency_account_by_currency(currency)
        money = source_currency_account.amount
        if money + quantity < 0:
            raise CannotTransfer(
                "Insufficient money, needs %d %s, have only %d %s" % (quantity, currency, money, currency))

        source_currency_account.amount += quantity
        source_currency_account.save()


# Unfortunately django-money does not allow selecting specific currency, so I'm rolling my own solution
class CurrencyAccount(models.Model):
    currency = models.CharField(choices=CURRENCIES_CHOICE, max_length=3)
    amount = models.DecimalField(max_digits=10, decimal_places=2, validators=[validators.MinValueValidator(0)],
                                 default=0)
    wallet = models.ForeignKey(Wallet, on_delete=models.CASCADE)

    class Meta:
        unique_together = (("currency", "wallet"),)


class Customer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE,
                                related_name='user_ext')
    wallet = models.ForeignKey(Wallet, on_delete=models.CASCADE,
                               related_name='user_wallet')

    def create_customer_data(sender, instance, created, **kwargs):
        if created:
            wallet = Wallet()
            wallet.save()
            Customer.objects.create(user=instance, wallet=wallet)

    post_save.connect(create_customer_data, sender=User)
