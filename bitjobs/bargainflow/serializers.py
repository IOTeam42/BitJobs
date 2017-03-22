from rest_framework import serializers
from taggit_serializer.serializers import TagListSerializerField, TaggitSerializer

from bargainflow.models import Commission, CommissionBid


class CommissionSerializer(TaggitSerializer, serializers.ModelSerializer):
    tags = TagListSerializerField()

    class Meta:
        model = Commission
        exclude = ('date_added',)


class CommissionBidSerializer(serializers.ModelSerializer):
    class Meta:
        model = CommissionBid
        exclude = ('date_added',)
