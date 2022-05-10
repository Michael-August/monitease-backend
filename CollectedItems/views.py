from unicodedata import name
from django.shortcuts import render, get_object_or_404
from .models import Apprentice, CollectedItems
from .serializers import ApprenticeSerializer, CollectedItemsSerializers
from rest_framework import generics, status
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend

# Create your views here.

class ApprenticeView(generics.GenericAPIView):
    serializer_class = ApprenticeSerializer
    name = "All Apprentice"
    queryset = Apprentice.objects.all()

    def get(self, request):
        apprentice = Apprentice.objects.all()
        serializer = self.serializer_class(instance=apprentice, many=True)
        return Response(data=serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        data = request.data
        serializer = self.serializer_class(data=data)

        if serializer.is_valid():
            serializer.save()
            return Response(data=serializer.data, status=status.HTTP_201_CREATED)

        return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class CollectedItemsListView(generics.GenericAPIView):
    serializer_class = CollectedItemsSerializers
    name = "Collected Items List"
    queryset = CollectedItems.objects.all()
    filter_backends = (DjangoFilterBackend,)

    filterset_fields = ('collectedBy', 'collectedFrom', 'havePaid', 'itemCollected',)

    def get(self, request):
        itemCollected = self.filter_queryset(self.get_queryset())
        serializer = self.serializer_class(instance=itemCollected, many=True)
        return Response(data=serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        data = request.data
        serializer = self.serializer_class(data=data)

        if serializer.is_valid():
            serializer.save()
            return Response(data=serializer.data, status=status.HTTP_201_CREATED)

        return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class CollectedItemsDetailView(generics.GenericAPIView):
    serializer_class = CollectedItemsSerializers
    name = "Details on Collected Item"

    def get(self, request, item_id):
        item = get_object_or_404(CollectedItems, pk=item_id)
        serializer = self.serializer_class(instance=item)
        return Response(data=serializer.data, status=status.HTTP_200_OK)

    def put(self, request, item_id):
        data = request.data
        item = get_object_or_404(CollectedItems, pk=item_id)
        serializer = self.serializer_class(data=data, instance=item)

        if serializer.is_valid():
            serializer.save()
            return Response(data=serializer.data, status=status.HTTP_200_OK)

        return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, item_id):
        item = get_object_or_404(CollectedItems, pk=item_id)
        item.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
