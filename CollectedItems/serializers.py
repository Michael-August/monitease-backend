from dataclasses import fields
from .models import CollectedItems, Apprentice
from rest_framework import serializers

class ApprenticeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Apprentice
        fields = "__all__"

class CollectedItemsSerializers(serializers.ModelSerializer):
    itemCollected = serializers.CharField(max_length=100)
    quantity = serializers.IntegerField()
    rate = serializers.IntegerField()
    totalPrice = serializers.IntegerField(read_only=True, default=0)
    collectedFrom = serializers.CharField(max_length=100)
    whoPicked = ApprenticeSerializer(read_only=True, many=True)
    havePaid = serializers.BooleanField(default=False)
    dateCollected = serializers.DateTimeField(read_only=True)
    datePaid = serializers.DateTimeField(read_only=True)

    class Meta:
        model = CollectedItems
        fields = "__all__"
