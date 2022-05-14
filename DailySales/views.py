import datetime
from django.shortcuts import get_object_or_404
from MonitEase.pagination import CustomPageNumberPagination
from rest_framework import generics, status
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from .serializers import DailySalesSerializer, ProductsSerializer, ScheduledSalesReportSerializer
from .models import DailySales, Products
from django.db.models import Sum

# Create your views here.

class ProductsView(generics.GenericAPIView):
    serializer_class = ProductsSerializer
    name = "Stock Items"
    queryset = Products.objects.all()

    def get(self, request):
        items = Products.objects.all()
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
    pagination_class = CustomPageNumberPagination
    queryset = DailySales.objects.all()
    name = 'Daily Sales List'
    filter_backends = (DjangoFilterBackend,)

    # filterset_fields = ('customername','havepaid', 'datesold', 'itemsold', 'datepaid')

    filterset_fields = {
        'datesold': ['gte', 'lte', 'exact'],
        'customername': ['exact'],
        'havepaid': ['exact'],
        'itemsold': ['exact'],
        'datepaid': ['gte', 'lte', 'exact']
    }

    def get(self, request):
        sales = self.filter_queryset(self.get_queryset())

        # Handling Pagination

        page = self.paginate_queryset(sales)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.serializer_class(instance=sales, many=True)
        return Response(data=serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        data = request.data
        serializer = self.serializer_class(data=data)

        if serializer.is_valid():
            serializer.save()

            item_sold_quantity = serializer.data.get('quantity')
            item_sold = Products.objects.get(pk=serializer.data.get('itemsold'))
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
            item_sold = Products.objects.get(pk=serializer.data.get('itemsold'))
            item_sold.quantity = item_sold.quantity - item_sold_quantity
            item_sold.save()

            return Response(data=serializer.data, status=status.HTTP_200_OK)

        return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, sales_id):
        sale = get_object_or_404(DailySales, pk=sales_id)
        sale.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class SalesFilteredReportView(generics.GenericAPIView):
    serializer_class = DailySalesSerializer
    name = 'Filterable Report'
    queryset = DailySales.objects.all()

    filter_backends = (DjangoFilterBackend,)

    filterset_fields = {
        'datesold': ['gte', 'lte']
    }

    def get(self, request):
        sales = self.filter_queryset(self.get_queryset())
        # sales = DailySales.objects.filter(datesold=datetime.datetime.now())
        total = DailySales.objects.aggregate(Sum('totalprice'))['totalprice__sum']
        print(total)
        serializer = self.serializer_class(instance=sales, many=True)
        return Response(data=serializer.data, status=status.HTTP_200_OK)


class SalesReportView(generics.GenericAPIView):
    serializer_class = DailySalesSerializer
    name = 'Report'
    queryset = DailySales.objects.all()

    def get(self, reques):
        sales = DailySales.objects.filter(datesold=datetime.datetime.today())
        total = DailySales.objects.aggregate(Sum('totalprice'))['totalprice__sum']
        print(total)
        serializer = self.serializer_class(instance=sales, many=True)
        return Response(data=serializer.data, status=status.HTTP_200_OK)


class ScheduledSalesReportView(generics.GenericAPIView):
    # serializer_class = ScheduledSalesReportSerializer
    # name = 'Report'
    # queryset = DailySales.objects.all()

    # def get(self,request):
    #     report = DailySales.objects.all()
    #     serializer = self.serializer_class(instance=report, many=True)
    #     return Response(data=serializer.data, status=status.HTTP_200_OK)
    pass

