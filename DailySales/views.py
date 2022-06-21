import datetime
from django.shortcuts import get_object_or_404
from MonitEase.pagination import CustomPageNumberPagination
from django.db.models import Sum

from rest_framework import generics, status
from rest_framework.decorators import permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend

from .serializers import DailySalesSerializer, ProductsSerializer, UpdateDatePaidSerializer
from .models import DailySales, Products

# Imports for pdf generating
from django.http import FileResponse
import io
from reportlab.pdfgen import canvas
from reportlab.lib.units import inch
from reportlab.lib.pagesizes import letter

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
    

class UpdateHavePaid(generics.GenericAPIView):
    serializer_class = UpdateDatePaidSerializer
    name = 'Update Have Paid'
    
    def put(self, request, sales_id):
        data = request.data
        sale = DailySales.objects.get(pk=sales_id)
        
        sale.havepaid = data.get('havepaid', sale.havepaid)
        sale.datepaid = data.get('datepaid', sale.datepaid)

        serializer = self.serializer_class(data=data, instance=sale)
        if serializer.is_valid():
            serializer.save()

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
        total = sales.aggregate(Sum('totalprice'))['totalprice__sum']
        have_paid_total = sales.filter(havepaid=True).aggregate(Sum('totalprice'))['totalprice__sum']
        if total == None:
            total = 0

        if have_paid_total == None:
            have_paid_total = 0
            
        unpaid_total = total - have_paid_total
        print(total, have_paid_total)
        print(total)
        serializer = self.serializer_class(instance=report, many=True)
        return Response(data={'data': serializer.data, 'total': total, 'paid_total': have_paid_total, 'credit_amount': unpaid_total}, status=status.HTTP_200_OK)


class SalesReportView(generics.GenericAPIView):
    serializer_class = DailySalesSerializer
    name = 'Report'
    queryset = DailySales.objects.all()

    def get(self, reques):
        sales = DailySales.objects.filter(datesold=datetime.datetime.today())
        total = DailySales.objects.filter(datesold=datetime.datetime.today()).aggregate(Sum('totalprice'))['totalprice__sum']
        have_paid_total = sales.filter(havepaid=True).aggregate(Sum('totalprice'))['totalprice__sum']
        if total == None:
            total = 0

        if have_paid_total == None:
            have_paid_total = 0

        unpaid_total = total - have_paid_total
        print(total, have_paid_total)
        serializer = self.serializer_class(instance=sales, many=True)
        return Response(data={'data': serializer.data, 'total': total, 'paid_total': have_paid_total, 'credit_amount': unpaid_total}, status=status.HTTP_200_OK)

    def report_pdf(self, request):

        sales = DailySales.objects.filter(datesold=datetime.datetime.today())
        total = DailySales.objects.filter(datesold=datetime.datetime.today()).aggregate(Sum('totalprice'))['totalprice__sum']
        print(total)
        serializer = self.serializer_class(instance=sales, many=True)

        # Create a buffer
        buf = io.BytesIO()

        # Create a canvas
        canva = canvas.Canvas(buf, pagesize=letter, bottomup=0)

        # Create a text object
        textOb = canva.beginText()
        textOb.setTextOrigin(inch, inch)
        textOb.setFont("Helvetica", 14)

        # Add lines of text
        for item in serializer.data:
            textOb.textLine(item)

        canva.drawText(textOb)
        canva.showPage()
        canva.save()
        buf.seek(0)

        return FileResponse(buf, as_attachment=True, filename='daily_report.pdf')


class MonthlyReportView(generics.GenericAPIView):
    serializer_class = DailySalesSerializer
    name = 'Monthly Report'
    queryset = DailySales.objects.all()


    def get(self,request):
        last_30days = datetime.datetime.today() - datetime.timedelta(30)
        report = DailySales.objects.filter(datesold__gte=last_30days)
        total = report.aggregate(Sum('totalprice'))['totalprice__sum']
        have_paid_total = report.filter(havepaid=True).aggregate(Sum('totalprice'))['totalprice__sum']
        if total == None:
            total = 0

        if have_paid_total == None:
            have_paid_total = 0
            
        unpaid_total = total - have_paid_total
        print(total, have_paid_total)
        print(total)
        serializer = self.serializer_class(instance=report, many=True)
        return Response(data={'data': serializer.data, 'total': total, 'paid_total': have_paid_total, 'credit_amount': unpaid_total}, status=status.HTTP_200_OK)


class WeeklyReportView(generics.GenericAPIView):
    serializer_class = DailySalesSerializer
    name = 'Weekly Report'
    queryset = DailySales.objects.all()


    def get(self,request):
        last_7days = datetime.datetime.today() - datetime.timedelta(7)
        report = DailySales.objects.filter(datesold__gte=last_7days)
        total = report.aggregate(Sum('totalprice'))['totalprice__sum']
        have_paid_total = report.filter(havepaid=True).aggregate(Sum('totalprice'))['totalprice__sum']
        if total == None:
            total = 0

        if have_paid_total == None:
            have_paid_total = 0
            
        unpaid_total = total - have_paid_total
        print(total, have_paid_total)
        serializer = self.serializer_class(instance=report, many=True)
        return Response(data={'data': serializer.data, 'total': total, 'paid_total': have_paid_total, 'credit_amount': unpaid_total}, status=status.HTTP_200_OK)


