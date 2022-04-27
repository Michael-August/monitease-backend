from unicodedata import name
from django.shortcuts import render, get_object_or_404
from rest_framework import generics, status
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from .serializers import DailySalesSerializer, ItemSoldSerializer
from .models import DailySales, ItemSold

# Create your views here.

class ItemsSoldView(generics.GenericAPIView):
    serializer_class = ItemSoldSerializer
    name = "Stock Items"
    queryset = ItemSold.objects.all()

    def get(self, request):
        items = ItemSold.objects.all()
        serializer = self.serializer_class(instance=items, many=True)
        return Response(data=serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        data = request.data
        serializer = self.serializer_class(data=data)

        if serializer.is_valid():
            serializer.save()
            return Response(data=serializer.data, status=status.HTTP_201_CREATED)

        return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class DailySalesListView(generics.GenericAPIView):
    serializer_class = DailySalesSerializer
    queryset = DailySales.objects.all()
    name = 'Daily Sales List'
    filter_backends = (DjangoFilterBackend,)

    filterset_fields = ('customername','havepaid', 'datesold', 'itemsold', 'datepaid')

    def get(self, request):
        sales = self.filter_queryset(self.get_queryset())
        serializer = self.serializer_class(instance=sales, many=True)
        return Response(data=serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        data = request.data
        serializer = self.serializer_class(data=data)

        if serializer.is_valid():
            serializer.save()

            item_sold_quantity = serializer.data.get('quantity')
            item_sold = ItemSold.objects.get(pk=serializer.data.get('itemsold'))
            item_sold.quantity = item_sold.quantity - item_sold_quantity
            item_sold.save()

            return Response(data=serializer.data, status=status.HTTP_201_CREATED)

        return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

class DailySalesDetailView(generics.GenericAPIView):
    serializer_class = DailySalesSerializer
    name = 'Get by Id and Delete Daily Sales'

    def get(self, request, sales_id):
        sales = get_object_or_404(DailySales, pk=sales_id)
        serializer = self.serializer_class(instance=sales)
        return Response(data=serializer.data, status=status.HTTP_200_OK)

    def put(self, request, sales_id):
        data = request.data
        sale = get_object_or_404(DailySales, pk=sales_id)

        serializer = self.serializer_class(data=data, instance=sale)
        if serializer.is_valid():
            serializer.save()
            
            item_sold_quantity = serializer.data.get('quantity')
            item_sold = ItemSold.objects.get(pk=serializer.data.get('itemsold'))
            item_sold.quantity = item_sold.quantity - item_sold_quantity
            item_sold.save()

            return Response(data=serializer.data, status=status.HTTP_200_OK)

        return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, sales_id):
        sale = get_object_or_404(DailySales, pk=sales_id)
        sale.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

