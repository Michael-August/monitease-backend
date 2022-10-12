from django.shortcuts import render

from django.shortcuts import get_object_or_404
from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from AuthArea.backends_auth import JWTAuthentication
from .serializers import (  ProductsSerializer, 
                            UpdateProductQuantitySerializer )

from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters
from .models import Products

# Create your views here.

class ProductsView(generics.GenericAPIView):
    serializer_class = ProductsSerializer
    queryset = Products.objects.all().order_by('-dateadded')
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    filter_backends = (DjangoFilterBackend, filters.SearchFilter,)
    search_fields = ['item_name', 'quantity']

    filterset_fields = {
        'quantity': ['exact'],
        'item_name': ['exact'],
        'total_added': ['exact']
    }
    
    name = "Stock Items"
    queryset = Products.objects.all()

    def get(self, request):
        items = self.filter_queryset(self.get_queryset())
        serializer = self.serializer_class(instance=items, many=True)
        return Response(data=serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        try:
            if request.user.role == 'OTHERS':
                response = {
                    'success': False,
                    'status_code': status.HTTP_403_FORBIDDEN,
                    'message': 'You are not authorized to perform this action'
                }
                return Response(response, status=status.HTTP_403_FORBIDDEN)
            else:
                data = request.data
                product_exist = Products.objects.filter(item_name = data.get('item_name')).count()
                serializer = self.serializer_class(data=data)
                
                if product_exist > 0:
                    response = {
                        'success': False,
                        'message': 'Product already exist'
                    }
                    return Response(data=response, status=status.HTTP_400_BAD_REQUEST)

                if serializer.is_valid():
                    
                    serializer.save()

                    response = {
                        'success': True,
                        'status_code': status.HTTP_201_CREATED,
                        'message': 'Product added successfuly',
                        'data': serializer.data
                    }
                    return Response(data=response, status=status.HTTP_201_CREATED)
        except:
            response = {
                'success': False,
                'status_code': status.HTTP_400_BAD_REQUEST,
                'message': 'Check your request and try again'
            }
            return Response(response, status=status.HTTP_400_BAD_REQUEST)


class ProductsDetailView(generics.GenericAPIView):
    serializer_class = ProductsSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    def get(self, request, product_id):
        product = get_object_or_404(Products, pk=product_id)
        serializer = self.serializer_class(instance=product)
        response = {
            'success': True,
            'status_code': status.HTTP_200_OK,
            'message': 'product fetched successfully',
            'data': serializer.data
        }
        return Response(response, status=status.HTTP_200_OK)

    def put(self, request, product_id):
        try:
            if request.user.role != 'DIRECTOR' and request.user.role != 'ADMIN':
                response = {
                    'success': False,
                    'status_code': status.HTTP_403_FORBIDDEN,
                    'message': 'You are not authorized to perform this action'
                }
                return Response(response, status=status.HTTP_403_FORBIDDEN)
            else:
                data = request.data
                product = get_object_or_404(Products, pk=product_id)
                difference = product.quantity - data.get('quantity')

                serializer = self.serializer_class(data=data, instance=product)

                if data.get('quantity') < product.quantity:
                    product.total_added = product.total_added - difference
                elif data.get('quantity') > product.quantity:
                    product.total_added = product.total_added + difference
                else:
                    product.total_added = product.total_added

                if serializer.is_valid():
                    product.save()
                    serializer.save()

                    response = {
                        'success': True,
                        'status_code': status.HTTP_200_OK,
                        'message': 'Product updated successfully',
                        'data': serializer.data
                    }
                    
                    return Response(response, status=status.HTTP_200_OK)
        except Exception as e:
            response = {
                'success': False,
                'status_code': status.HTTP_400_BAD_REQUEST,
                'message': 'Check your request and try again ' + str(e)
            }
            return Response(response, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, product_id):
        try:
            if request.user.role != 'DIRECTOR' and request.user.role != 'ADMIN':
                response = {
                    'success': False,
                    'status_code': status.HTTP_403_FORBIDDEN,
                    'message': 'You are not authorized to perform this action'
                }
                return Response(response, status=status.HTTP_403_FORBIDDEN)
            else:
                product = get_object_or_404(Products, pk=product_id)

                product.delete()
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


class UpdateProductQuantity(generics.GenericAPIView):
    serializer_class = UpdateProductQuantitySerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]
    name = 'Update Product Quantity'
    
    def patch(self, request, product_id):
        try:
            if request.user.role != 'DIRECTOR' and request.user.role != 'ADMIN':
                response = {
                    'success': False,
                    'status_code': status.HTTP_403_FORBIDDEN,
                    'message': 'You are not authorized to perform this action'
                }
                return Response(response, status=status.HTTP_403_FORBIDDEN)
            else:
                data = request.data
                product = Products.objects.get(pk=product_id)
                
                product.total_added = product.total_added + data.get('quantity')
                product.quantity = data.get('quantity') + product.quantity
                product.datupdated = data.get('dateupdated')

                product.save()
                serializer = self.serializer_class(product)
                
                response = {
                    'success': True,
                    'status_code': status.HTTP_200_OK,
                    'message': 'Product quantity updated successfully',
                    'data': serializer.data
                }
                
                return Response(response, status=status.HTTP_200_OK)
        except:
            response = {
                'success': False,
                'status_code': status.HTTP_400_BAD_REQUEST,
                'message': 'Check your request and try again'
            }
            return Response(response, status=status.HTTP_400_BAD_REQUEST)
