from dataclasses import fields
from .models import DailySales
from Products.serializers import ProductsSerializer
from rest_framework import serializers

class DailySalesSerializer(serializers.ModelSerializer):
    customername = serializers.CharField(max_length=100)
    soldItem = ProductsSerializer(read_only=True, many=True)
    quantity = serializers.IntegerField()
    rate = serializers.IntegerField()
    totalprice = serializers.IntegerField(default=0, read_only=True)
    datesold = serializers.DateField(read_only=True)
    paymentmethod = serializers.CharField(max_length=40)
    havepaid = serializers.BooleanField(default=False)
    datepaid = serializers.DateField(read_only=True)

    class Meta:
        model = DailySales
        fields = "__all__"

class UpdateDatePaidSerializer(serializers.ModelSerializer):
    paymentmethod = serializers.CharField(max_length=40)
    havepaid = serializers.BooleanField(default=False)
    datepaid = serializers.DateField()


    class Meta:
        model = DailySales
        fields = "__all__"
    

