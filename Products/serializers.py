from dataclasses import fields
from .models import Products
from rest_framework import serializers

class ProductsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Products
        fields= "__all__"

class UpdateProductQuantitySerializer(serializers.ModelSerializer):
    quantity = serializers.IntegerField()
    dateupdated = serializers.DateField()

    class Meta:
        model = Products
        fields = "__all__"