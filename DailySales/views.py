import datetime
from os import abort
from django.shortcuts import get_object_or_404
from MonitEase.pagination import CustomPageNumberPagination
from django.db.models import Sum

from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters

from AuthArea.backends_auth import JWTAuthentication

from .serializers import (  DailySalesSerializer, 
                            UpdateDatePaidSerializer )
from .models import DailySales
from Products.models import Products

# Imports for pdf generating
from django.http import FileResponse
import io
from reportlab.pdfgen import canvas
from reportlab.lib.units import inch
from reportlab.lib.pagesizes import letter

# Create your views here.
            

class DailySalesListView(generics.GenericAPIView):
    serializer_class = DailySalesSerializer
    pagination_class = CustomPageNumberPagination
    queryset = DailySales.objects.all().order_by('-datesold')
    # queryset = DailySales.objects.raw('SELECT s.id, p.item_name, s.rate, s.customername, s.quantity, s.datesold, s.havepaid, s.datepaid, s.paymentmethod from DailySales_dailysales s join Products_products p on s.itemsold_id=p.id')
    name = 'Daily Sales List'
    filter_backends = (DjangoFilterBackend, filters.SearchFilter,)
    search_fields = ['customername', 'itemsold__item_name']
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]

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
        try:
            if request.user.role != 'SECRATARY' and request.user.role != 'ADMIN':
                response = {
                    'success': False,
                    'status_code': status.HTTP_403_FORBIDDEN,
                    'message': 'You are not authorized to perform this action'
                }
                return Response(response, status=status.HTTP_403_FORBIDDEN)
            else:
                data = request.data
                serializer = self.serializer_class(data=data)

                if serializer.is_valid():
                    if data.get('havepaid') == True:
                        # DailySales.datepaid = data.get('datesold')
                        # DailySales.save()
                        pass

                    serializer.save()

                    item_sold_quantity = serializer.data.get('quantity')
                    item_sold = Products.objects.get(pk=serializer.data.get('itemsold'))
                    item_sold.quantity = item_sold.quantity - item_sold_quantity
                    item_sold.save()

                    response = {
                        'success': True,
                        'status_code': status.HTTP_201_CREATED,
                        'message': 'Sale added successfuly',
                        'data': serializer.data
                    }
                    return Response(response, status=status.HTTP_201_CREATED)
        except Exception as e:
            response = {
                'success': False,
                'status_code': status.HTTP_400_BAD_REQUEST,
                'message': 'Check your request and try again',
                'error': str(e)
            }
            return Response(response, status=status.HTTP_400_BAD_REQUEST)
    

class UpdateHavePaid(generics.GenericAPIView):
    serializer_class = UpdateDatePaidSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]
    name = 'Update Have Paid'
    
    def patch(self, request, sales_id):
        try:
            if request.user.role != 'SECRATARY' and request.user.role != 'ADMIN':
                response = {
                    'success': False,
                    'status_code': status.HTTP_403_FORBIDDEN,
                    'message': 'You are not authorized to perform this action'
                }
                return Response(response, status=status.HTTP_403_FORBIDDEN)
            else:
                data = request.data
                sale = DailySales.objects.get(pk=sales_id)

                # serializer = self.serializer_class(data=data)
                # if serializer.is_valid():
                print(data.get('havepaid'))
                sale.havepaid = data.get('havepaid')

                if data.get('paymentmethod'):
                    sale.paymentmethod = data.get('paymentmethod')
                    sale.datepaid = data.get('datepaid')

                sale.paymentmethod = sale.paymentmethod
                sale.datepaid = sale.datepaid
                sale.save()

                response = {
                    'success': True,
                    'status_code': status.HTTP_200_OK,
                    'message': 'Paid status updated successfully',
                }
            
                return Response(response, status=status.HTTP_200_OK)
        except Exception as e:
            response = {
                'success': False,
                'status_code': status.HTTP_400_BAD_REQUEST,
                'message': 'Check your request and try again',
                'error': str(e)
            }
            return Response(data=response, status=status.HTTP_400_BAD_REQUEST)
        

class DailySalesDetailView(generics.GenericAPIView):
    serializer_class = DailySalesSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]
    name = 'Get by Id and Delete Daily Sales'

    def get(self, request, sales_id):
        sales = get_object_or_404(DailySales, pk=sales_id)
        serializer = self.serializer_class(instance=sales)
        return Response(data=serializer.data, status=status.HTTP_200_OK)

    def put(self, request, sales_id):
        try:
            if request.user.role != 'SECRATARY' and request.user.role != 'ADMIN':
                response = {
                    'success': False,
                    'status_code': status.HTTP_403_FORBIDDEN,
                    'message': 'You are not authorized to perform this action'
                }
                return Response(response, status=status.HTTP_403_FORBIDDEN)
            data = request.data
            sale = get_object_or_404(DailySales, pk=sales_id)

            serializer = self.serializer_class(data=data, instance=sale)
            if serializer.is_valid():
                serializer.save()
                
                # item_sold_quantity = serializer.data.get('quantity')
                # item_sold = Products.objects.get(pk=serializer.data.get('itemsold'))
                # item_sold.quantity = item_sold.quantity - item_sold_quantity
                # item_sold.save()

            return Response(data=serializer.data, status=status.HTTP_200_OK)
        except:
            return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, sales_id):
        try:
            if request.user.role != 'SECRATARY' and request.user.role != 'ADMIN':
                response = {
                    'success': False,
                    'status_code': status.HTTP_403_FORBIDDEN,
                    'message': 'You are not authorized to perform this action'
                }
                return Response(response, status=status.HTTP_403_FORBIDDEN)
            else:
                sale = get_object_or_404(DailySales, pk=sales_id)

                sale.delete()
                response = {
                    'success': True,
                    'status_code': status.HTTP_204_NO_CONTENT,
                    'message': 'Product deleted successfully'
                }
                return Response(response, status=status.HTTP_204_NO_CONTENT)
        except:
            response = {
                'success': False,
                'status_code': status.HTTP_400_BAD_REQUEST,
                'message': 'Check your request and try again'
            }
            return Response(response, status=status.HTTP_400_BAD_REQUEST)


class SalesFilteredReportView(generics.GenericAPIView):
    serializer_class = DailySalesSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]
    name = 'Filterable Report'
    queryset = DailySales.objects.all().order_by('-datesold')

    filter_backends = (DjangoFilterBackend,)

    filterset_fields = {
        'datesold': ['gte', 'lte']
    }

    def get(self, request):
        if request.user.role == 'OTHERS':
            response = {
                    'success': False,
                    'status_code': status.HTTP_403_FORBIDDEN,
                    'message': 'You are not authorized to perform this action'
                }
            return Response(response, status=status.HTTP_403_FORBIDDEN)
        else:
            sales = self.filter_queryset(self.get_queryset())
            total = sales.aggregate(Sum('totalprice'))['totalprice__sum']
            have_paid_total = sales.filter(havepaid=True).aggregate(Sum('totalprice'))['totalprice__sum']
            transfer_total = sales.filter(havepaid=True).filter(paymentmethod='transfer').aggregate(Sum('totalprice'))['totalprice__sum']
            cash_total = sales.filter(havepaid=True).filter(paymentmethod='cash').aggregate(Sum('totalprice'))['totalprice__sum']

            if total == None:
                total = 0

            if have_paid_total == None:
                have_paid_total = 0

            if transfer_total == None:
                transfer_total = 0

            if cash_total == None:
                cash_total = 0
                
            unpaid_total = total - have_paid_total
            serializer = self.serializer_class(instance=sales, many=True)
            return Response(data={'data': serializer.data, 'total': total, 'paid_total': have_paid_total, 'credit_amount': unpaid_total, 'total_transfer': transfer_total, 'total_cash': cash_total}, status=status.HTTP_200_OK)


class SalesReportView(generics.GenericAPIView):
    serializer_class = DailySalesSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]
    name = 'Report'
    queryset = DailySales.objects.all().order_by('datesold')

    def get(self, request):
        if request.user.role == 'OTHERS':
            response = {
                    'success': False,
                    'status_code': status.HTTP_403_FORBIDDEN,
                    'message': 'You are not authorized to perform this action'
                }
            return Response(response, status=status.HTTP_403_FORBIDDEN)
        else:
            sales = DailySales.objects.filter(datesold=datetime.datetime.today())
            total = DailySales.objects.filter(datesold=datetime.datetime.today()).aggregate(Sum('totalprice'))['totalprice__sum']
            have_paid_total = sales.filter(havepaid=True).aggregate(Sum('totalprice'))['totalprice__sum']
            transfer_total = sales.filter(havepaid=True).filter(paymentmethod='transfer').aggregate(Sum('totalprice'))['totalprice__sum']
            cash_total = sales.filter(havepaid=True).filter(paymentmethod='cash').aggregate(Sum('totalprice'))['totalprice__sum']

            if total == None:
                total = 0

            if have_paid_total == None:
                have_paid_total = 0

            if transfer_total == None:
                transfer_total = 0

            if cash_total == None:
                cash_total = 0

            unpaid_total = total - have_paid_total
            print(total, have_paid_total)
            serializer = self.serializer_class(instance=sales, many=True)
            return Response(data={'data': serializer.data, 'total': total, 'paid_total': have_paid_total, 'credit_amount': unpaid_total, 'total_transfer': transfer_total, 'total_cash': cash_total}, status=status.HTTP_200_OK)

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
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]
    name = 'Monthly Report'
    queryset = DailySales.objects.all().order_by('-datesold')


    def get(self,request):
        if request.user.role == 'OTHERS':
            response = {
                    'success': False,
                    'status_code': status.HTTP_403_FORBIDDEN,
                    'message': 'You are not authorized to perform this action'
                }
            return Response(response, status=status.HTTP_403_FORBIDDEN)
        else:
            last_30days = datetime.datetime.today() - datetime.timedelta(30)
            report = DailySales.objects.filter(datesold__gte=last_30days)
            total = report.aggregate(Sum('totalprice'))['totalprice__sum']
            have_paid_total = report.filter(havepaid=True).aggregate(Sum('totalprice'))['totalprice__sum']
            transfer_total = report.filter(havepaid=True).filter(paymentmethod='transfer').aggregate(Sum('totalprice'))['totalprice__sum']
            cash_total = report.filter(havepaid=True).filter(paymentmethod='cash').aggregate(Sum('totalprice'))['totalprice__sum']

            if total == None:
                total = 0

            if have_paid_total == None:
                have_paid_total = 0

            if transfer_total == None:
                transfer_total = 0

            if cash_total == None:
                cash_total = 0
                
            unpaid_total = total - have_paid_total
            serializer = self.serializer_class(instance=report, many=True)
            return Response(data={'data': serializer.data, 'total': total, 'paid_total': have_paid_total, 'credit_amount': unpaid_total, 'total_transfer': transfer_total, 'total_cash': cash_total}, status=status.HTTP_200_OK)


class WeeklyReportView(generics.GenericAPIView):
    serializer_class = DailySalesSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]
    name = 'Weekly Report'
    queryset = DailySales.objects.all().order_by('-datesold')


    def get(self,request):
        if request.user.role == 'OTHERS':
            response = {
                    'success': False,
                    'status_code': status.HTTP_403_FORBIDDEN,
                    'message': 'You are not authorized to perform this action'
                }
            return Response(response, status=status.HTTP_403_FORBIDDEN)
        else:
            last_7days = datetime.datetime.today() - datetime.timedelta(7)
            report = DailySales.objects.filter(datesold__gte=last_7days)
            total = report.aggregate(Sum('totalprice'))['totalprice__sum']
            have_paid_total = report.filter(havepaid=True).aggregate(Sum('totalprice'))['totalprice__sum']
            transfer_total = report.filter(havepaid=True).filter(paymentmethod='transfer').aggregate(Sum('totalprice'))['totalprice__sum']
            cash_total = report.filter(havepaid=True).filter(paymentmethod='cash').aggregate(Sum('totalprice'))['totalprice__sum']

            if total == None:
                total = 0

            if have_paid_total == None:
                have_paid_total = 0

            if transfer_total == None:
                transfer_total = 0

            if cash_total == None:
                cash_total = 0
                
            unpaid_total = total - have_paid_total
            serializer = self.serializer_class(instance=report, many=True)
            return Response(data={'data': serializer.data, 'total': total, 'paid_total': have_paid_total, 'credit_amount': unpaid_total, 'total_transfer': transfer_total, 'total_cash': cash_total}, status=status.HTTP_200_OK)


