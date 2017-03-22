from rest_framework import viewsets

from bargainflow.models import Commission, CommissionBid
from bargainflow.serializers import CommissionBidSerializer, \
    CommissionSerializer


class CommissionViewSet(viewsets.ModelViewSet):
    """
    Commissions endpoint.
    """
    queryset = Commission.objects.all()
    serializer_class = CommissionSerializer


class CommissionBidViewSet(viewsets.ModelViewSet):
    """
    Commission bids endpoint.
    """
    queryset = CommissionBid.objects.all()
    serializer_class = CommissionBidSerializer
