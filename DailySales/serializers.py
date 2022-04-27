from dataclasses import fields
from .models import DailySales, ItemSold
from rest_framework import serializers

class ItemSoldSerializer(serializers.ModelSerializer):
    class Meta:
        model = ItemSold
        fields= "__all__"

class DailySalesSerializer(serializers.ModelSerializer):
    customername = serializers.CharField(max_length=100)
    soldItem = ItemSoldSerializer(read_only=True, many=True)
    quantity = serializers.IntegerField()
    rate = serializers.IntegerField()
    totalprice = serializers.IntegerField(default=0, read_only=True)
    datesold = serializers.DateTimeField(read_only=True)
    paymentmethod = serializers.CharField(max_length=40)
    havepaid = serializers.BooleanField(default=False)
    datepaid = serializers.DateTimeField(read_only=True)

    class Meta:
        model = DailySales
        fields = "__all__"
    
