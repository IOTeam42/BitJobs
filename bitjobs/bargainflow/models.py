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

from django.db import models
from django.contrib.auth.models import User

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
    description = models.TextField()
    status = models.CharField(max_length=1, choices=COMMISSION_STATUS,
                              default=COMMISSION_STATUS[0][0])
    # money field

    tags = TaggableManager()


class CommissionBid(models.Model):
    commission = models.ForeignKey(Commission, models.CASCADE, null=False)
    bidder = models.ForeignKey(User, models.CASCADE)
    date_added = models.DateField(auto_now_add=True, null=False)
    bidder_comment = models.TextField()
