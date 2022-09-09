from dataclasses import fields

from DailySales.serializers import DailySalesSerializer
from .models import Products
from rest_framework import serializers

class ProductsSerializer(serializers.ModelSerializer):
    soldItem = DailySalesSerializer(many=True, read_only=True)
    class Meta:
        model = Products
        fields= "__all__"

class UpdateProductQuantitySerializer(serializers.ModelSerializer):
    quantity = serializers.IntegerField()
    dateupdated = serializers.DateField()

    class Meta:
        model = Products
        fields = "__all__"