from django.test import TestCase
from bitjobs.settings import CURRENCIES
from .models import Wallet, CurrencyAccount, CannotTransfer


# Create your tests here.

class WalletTest(TestCase):
    def setUp(self):
        self.wallet = Wallet.objects.create()
        self.target = Wallet.objects.create()
        self.currency = CURRENCIES[0][0]

    def test_creating_wallet_creates_currency_accounts(self):
        numberOfCurrrencyAccounts = CurrencyAccount.objects.all().count()
        Wallet.objects.create()
        self.assertEquals(CurrencyAccount.objects.all().count(),
                          numberOfCurrrencyAccounts + len(CURRENCIES))

    def test_saving_wallet_again_does_not_create_currency_accounts(self):
        numberOfCurrrencyAccounts = CurrencyAccount.objects.all().count()
        self.wallet.save()
        self.assertEquals(numberOfCurrrencyAccounts,
                          CurrencyAccount.objects.all().count())

    def test_money_by_currency_throws_on_invalid_currency(self):
        with self.assertRaises(ValueError):
            self.wallet.money_by_currency("sdaga")

    def test_money_by_currency_returns_correct_value(self):
        account = self.wallet.currencyaccount_set \
            .filter(currency__exact=self.currency).first()
        account.amount = 10
        account.save()

        self.assertEquals(self.wallet.money_by_currency(self.currency), 10)

    def test_transfer_raises_on_invalid_currency(self):
        with self.assertRaises(ValueError):
            self.wallet.transfer(None, "asdf", 0)

    def test_transfer_raises_when_too_little_money(self):
        currency_account = self.wallet.currencyaccount_set \
            .filter(currency__exact=self.currency).first()
        currency_account.amount = 0
        currency_account.save()
        with self.assertRaises(CannotTransfer):
            self.wallet.transfer(self.target, self.currency, 10)

    def test_transfer_works(self):
        currency_account = self.wallet.currencyaccount_set \
            .filter(currency__exact=self.currency).first()
        currency_account.amount = 15
        currency_account.save()
        target_money_before = self.target.money_by_currency(self.currency)
        self.wallet.transfer(self.target, self.currency, 10)
        self.assertEqual(self.wallet.money_by_currency(self.currency), 5)
        self.assertEqual(self.target.money_by_currency(self.currency),
                         target_money_before + 10)
