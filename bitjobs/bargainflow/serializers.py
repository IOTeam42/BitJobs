from rest_framework import serializers

from bargainflow.models import Commission, CommissionBid


class CommissionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Commission
        exclude = ('date_added',)


class CommissionBidSerializer(serializers.ModelSerializer):
    class Meta:
        model = CommissionBid
        exclude = ('date_added',)
