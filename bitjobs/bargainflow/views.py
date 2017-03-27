from rest_framework import viewsets
from rest_framework.decorators import permission_classes
from rest_framework.permissions import IsAuthenticated

from bargainflow.permissions import CommissionPermission
from bargainflow.models import Commission, CommissionBid
from bargainflow.serializers import CommissionBidSerializer, \
    CommissionSerializer


class CommissionViewSet(viewsets.ModelViewSet):
    """
    Commissions endpoint.
    """
    queryset = Commission.objects.all()
    serializer_class = CommissionSerializer
    permission_classes = (CommissionPermission,)


class CommissionBidViewSet(viewsets.ModelViewSet):
    """
    Commission bids endpoint.
    """
    queryset = CommissionBid.objects.all()
    serializer_class = CommissionBidSerializer
