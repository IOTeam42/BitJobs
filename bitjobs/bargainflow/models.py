"""
Module for storing data about commissions.
By commission we will mean a task to perform
for a given price.

Commission model stores main data about
commission, whereas Commission bid is an offer
made by other users to perform given task
"""

from __future__ import unicode_literals

from collections import defaultdict
from datetime import datetime

from django.contrib.auth.models import User
from django.db import models
from django.utils.translation import ugettext_lazy as _
from djmoney.models.fields import MoneyField
from taggit.managers import TaggableManager

class Commission(models.Model):
    COMMISSION_STATUS = (
        ('O', 'Opened'),
        ('B', 'Bidded'),
        ('A', 'Accepted'),
        ('F', 'Finished')
    )

    VALID_TRANSITION = defaultdict(list, {
        'O': ['B'],
        'B': ['A'],
        'A': ['F', 'B'],
        'F': [],
    })

    orderer = models.ForeignKey(User, null=False, related_name='orderer')
    contractor = models.ForeignKey(User, null=True, related_name='contractor')
    date_added = models.DateField(default=datetime.now(), null=False)
    title = models.CharField(_("Title"), max_length=40)
    description = models.TextField(_("Offer description"))
    status = models.CharField(max_length=1, choices=COMMISSION_STATUS,
                              default=COMMISSION_STATUS[0][0])
    price = MoneyField(max_digits=10, decimal_places=2, default_currency='PLN')
    tags = TaggableManager(_("Tags"))

    @property
    def commission_bids(self):
        return CommissionBid.objects.filter(commission=self)


class CommissionBid(models.Model):
    commission = models.ForeignKey(Commission, models.CASCADE, null=False)
    bidder = models.ForeignKey(User, models.CASCADE)
    date_added = models.DateField(auto_now_add=True, null=False)
    bidder_comment = models.TextField(_("Comment"))
